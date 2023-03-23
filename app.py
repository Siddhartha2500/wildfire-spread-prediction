import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def images(eval_data):
    # Create 64x64 grid of zeros
    prev_mask_grid = np.zeros( (64, 64,3), dtype=np.uint8)
    actual_fire_mask_grid = np.zeros( (64, 64,3),dtype=np.uint8)
    predicted_mask_grid = np.zeros( (64, 64,3),dtype=np.uint8)

    for i, row in eval_data.iterrows():
        row_number, column_index = int(row['row_index']), int(row['column_index'])
        # prev_mask = int(row['PrevFireMask'])
        # actual_mask  = int(row['FireMask'])
        # predicted_mask  = int(row['PredictedFireMask'])

        # print(row_number, column_index)
        #previous fire mask
        PF = int(row['PrevFireMask'])
        if PF == 1:
            prev_mask_grid[row_number,column_index] = [255,0,0]#red color
        elif PF == 0:
            prev_mask_grid[row_number,column_index] = [150, 146, 146]#gray color
        elif PF == -1:
            prev_mask_grid[row_number,column_index] = [0,0,0]#black color

        #firemask
        FM = int(row['FireMask'])
        if FM == 1:
            actual_fire_mask_grid[row_number, column_index] = [255,0,0]
        elif FM == 0:
            actual_fire_mask_grid[row_number, column_index] = [150, 146, 146]
        elif FM == -1:
            actual_fire_mask_grid[row_number, column_index] = [0,0,0]
        #predicted firemask
        PDF = int(row['PredictedFireMask'])
        if PDF == 1:
            predicted_mask_grid[row_number, column_index] = [255,0,0]
        elif PDF == 0:
            predicted_mask_grid[row_number, column_index] = [150, 146, 146]
        elif PDF == -1:
            predicted_mask_grid[row_number, column_index] = [0,0,0]
    return prev_mask_grid, actual_fire_mask_grid, predicted_mask_grid



#title
st.title("WildFire Predictions")

#set the image
st.image("wildfire.jpeg", caption = "Wildfire Preventing")

#upload a csv to predict
file = st.file_uploader("Please Upload a csv file")

if file:
    filename = file.name
    if not filename.endswith(".csv"):
        st.error("Please upload a CSV file", icon="🚨")
    else:
        wanted_columns = ['row_index','column_index','PrevFireMask','FireMask','PredictedFireMask']
        #read the data
        data = pd.read_csv(file)
        result = True
        for col in wanted_columns:
            if col not in list(data.columns):
                result = False
                break
        if not result:
            st.error("One of these columns are missing:{}".format(wanted_columns),icon="🚨")
        else:
            #show the dataset
            st.subheader("Uploaded Dataset")
            st.dataframe(data)

            #predictions as images
            st.subheader("Predictions through Images")
            #create three images
            prev_mask_grid, actual_fire_mask_grid, predicted_mask_grid = images(data)
            image_set = [prev_mask_grid,actual_fire_mask_grid,predicted_mask_grid]
            names = ['Previous Fire Mask','Actual Fire Mask','Predicted Fire Mask']
            fig = plt.figure(figsize = (8,8))
            for i in range(3):
                plt.subplot(1,3, i+1)
                plt.axis('off')
                plt.title(f"{names[i]}")
                plt.imshow(image_set[i], cmap = 'brg')
            #display the plot
            st.pyplot(fig)

            #column
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("🟥 - **Wildfire**")
                st.markdown("⬛️ - **Uncertain**")
                st.markdown("⬜️ - **No Wildfire**")
