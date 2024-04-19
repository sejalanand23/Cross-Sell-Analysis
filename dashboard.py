# import required libraries
import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from streamlit_extras.add_vertical_space import add_vertical_space

# set the page configuration
st.set_page_config(page_title='Cross-Sell Analysis', page_icon='🛒', layout='wide')

# create a title for your app
st.title('🛒 Cross-Sell Analysis')

# import data
df = pd.read_csv('association_rules.csv')


# Function to clean and extract items
def extract_items(s):
    # Remove curly braces, quotes, and brackets
    s = re.sub(r"[{}\[\]']", "", s)
    # Split by comma and strip spaces
    items = [item.strip() for item in s.split(",")]
    return items

# Clean and extract items from 'Antecedents' column
antecedents_items = df['Antecedents'].apply(extract_items).explode().unique()

# Clean and extract items from 'Consequents' column
consequents_items = df['Consequents'].apply(extract_items).explode().unique()


col1, col2, col3, col4 = st.columns([1,7,7,1])
with col2:
    antecedents = st.multiselect('Select Antecedents', antecedents_items)
with col3:
    consequents = st.multiselect('Select Consequents', consequents_items)

# show below only when the user selects the antecedents and consequents
if antecedents and consequents:

    # Subset of DataFrame based on mask
    mask = (df['Antecedents'].apply(lambda x: all(item in x for item in antecedents)) & 
            df['Consequents'].apply(lambda x: all(item in x for item in consequents)))

    subset_df = df[mask]

    if len(subset_df) == 0:
        c1, c2, c3 = st.columns(3)
        with c2:
            add_vertical_space(4)
            st.error("No records found for the selected combination.")

    else:
        # Count rows where Antecedents and Consequents are present
        left_count = df['Antecedents'].apply(lambda x: any(item in x for item in antecedents)).sum()
        right_count = df['Consequents'].apply(lambda x: any(item in x for item in consequents)).sum()

        # Create Venn diagram
        plt.figure(figsize=(5, 3))
        venn = venn2(subsets=(left_count, right_count, len(subset_df)), set_labels=(antecedents, consequents), normalize_to=0.1)
        venn.get_patch_by_id('10').set_color('#96b8e2')
        venn.get_patch_by_id('01').set_color('#ccb4d8')
        venn.get_patch_by_id('11').set_color('#a299d3')
        venn.get_label_by_id('10').set_text('{}\n ({}%)'.format(left_count, ((left_count/len(df))*100).round(2)))
        venn.get_label_by_id('01').set_text('{}\n ({}%)'.format(right_count, ((right_count/len(df))*100).round(2)))
        venn.get_label_by_id('11').set_text('{}\n ({}%)'.format(len(subset_df), round(((len(subset_df)/len(df))*100),2)))
        for text in venn.set_labels:
            text.set_fontsize(5)
        for text in venn.subset_labels:
            text.set_fontsize(3)

        fig1, fig2, fig3 = st.columns([1,5,3])
        with fig2:
            st.pyplot(plt)
        with fig3:
            add_vertical_space(9)
            st.info("{} is present in {}% of the baskets.".format(antecedents, round((left_count/len(df))*100, 2)))
            st.info("{} is present in {}% of the baskets.".format(consequents, round((right_count/len(df))*100, 2)))
            st.info("The combination of {} and {} is present in {}% of the baskets.".format(antecedents, consequents, round((len(subset_df)/len(df))*100, 2)))
