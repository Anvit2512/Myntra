from django.shortcuts import render
from .forms import SizeForm
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

def find_closest(df, measurements, size_columns):
    df['distance'] = df[size_columns].apply(lambda row: np.linalg.norm(row - measurements), axis=1)
    return df.nsmallest(10, 'distance')

def recommend(request):
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            chest = form.cleaned_data['chest']
            waist = form.cleaned_data['waist']
            hips = form.cleaned_data['hips']
            height_shoulder = form.cleaned_data['height_shoulder']
            height_hips = form.cleaned_data['height_hips']
            
            if gender == 'male':
                shirts_df = pd.read_csv(r'F:\datasets\separate_dataset\shirts.csv')
                jeans_df = pd.read_csv(r'F:\datasets\separate_dataset\jeans.csv')
                
                shirts_df['front_length'] = height_shoulder - height_hips
                shirts_df[['chest', 'waist', 'front_length']] = shirts_df[['chest', 'waist', 'front_length']].fillna(shirts_df[['chest', 'waist', 'front_length']].mean())
                
                jeans_df[['to_fit_waist', 'hips', 'outseam_length']] = jeans_df[['to_fit_waist', 'hips', 'outseam_length']].fillna(jeans_df[['to_fit_waist', 'hips', 'outseam_length']].mean())
                
                shirt_measurements = np.array([chest, waist, height_shoulder - height_hips])
                jeans_measurements = np.array([waist, hips, height_hips])
                
                closest_shirts = find_closest(shirts_df, shirt_measurements, ['chest', 'waist', 'front_length'])
                closest_jeans = find_closest(jeans_df, jeans_measurements, ['to_fit_waist', 'hips', 'outseam_length'])
                
                closest_shirts['image'] = closest_shirts['images'].apply(lambda x: np.random.choice(x.split(',')) if pd.notna(x) else None)
                closest_jeans['image'] = closest_jeans['images'].apply(lambda x: np.random.choice(x.split(',')) if pd.notna(x) else None)
                
                shirts_results = closest_shirts[['size', 'product_id', 'title', 'initial_price', 'category', 'image']]
                jeans_results = closest_jeans[['size', 'product_id', 'title', 'initial_price', 'category', 'image']]
                
                return render(request, 'recommend/results.html', {
                    'shirts_results': shirts_results,
                    'jeans_results': jeans_results,
                    'gender': gender
                })
            
            elif gender == 'female':
                tops_df = pd.read_csv(r'F:\datasets\separate_dataset\tops.csv')
                skirts_df = pd.read_csv(r'F:\datasets\separate_dataset\skirts.csv')
                
                tops_df['front_length'] = height_shoulder - height_hips
                tops_df[['to_fit_bust', 'to_fit_waist', 'front_length', 'chest', 'bust', 'waist']] = tops_df[['to_fit_bust', 'to_fit_waist', 'front_length', 'chest', 'bust', 'waist']].fillna(tops_df[['to_fit_bust', 'to_fit_waist', 'front_length', 'chest', 'bust', 'waist']].mean())
                
                skirts_df[['to_fit_hip', 'to_fit_waist']] = skirts_df[['to_fit_hip', 'to_fit_waist']].fillna(skirts_df[['to_fit_hip', 'to_fit_waist']].mean())
                
                tops_measurements = np.array([chest, waist, height_shoulder - height_hips, chest, chest, waist])
                skirts_measurements = np.array([hips, waist])
                
                closest_tops = find_closest(tops_df, tops_measurements, ['to_fit_bust', 'to_fit_waist', 'front_length', 'chest', 'bust', 'waist'])
                closest_skirts = find_closest(skirts_df, skirts_measurements, ['to_fit_hip', 'to_fit_waist'])
                
                closest_tops['image'] = closest_tops['images'].apply(lambda x: np.random.choice(x.split(',')) if pd.notna(x) else None)
                closest_skirts['image'] = closest_skirts['images'].apply(lambda x: np.random.choice(x.split(',')) if pd.notna(x) else None)
                
                tops_results = closest_tops[['size', 'product_id', 'title', 'initial_price', 'category', 'image']]
                skirts_results = closest_skirts[['size', 'product_id', 'title', 'initial_price', 'category', 'image']]
                
                return render(request, 'recommend/results.html', {
                    'tops_results': tops_results,
                    'skirts_results': skirts_results,
                    'gender': gender
                })
    else:
        form = SizeForm()
    return render(request, 'recommend.html', {'form': form})
