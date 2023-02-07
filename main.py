import streamlit as st
import pandas as pd
from io import BytesIO


def to_excel(data_frame):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data_frame.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


df_main_values = pd.DataFrame()
df_lookup_values = pd.DataFrame()

st.write("Look up values")

uploaded_file = st.file_uploader("Choose file", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        df_main_values = pd.read_excel(uploaded_file,
                                       sheet_name="main_values")
        df_lookup_values = pd.read_excel(uploaded_file,
                                         sheet_name="look_up_values",
                                         index_col=0,
                                         dtype=str)
    else:
        df_main_values = pd.read_excel(uploaded_file,
                                       sheet_name="main_values")
        df_lookup_values = pd.read_excel(uploaded_file,
                                         sheet_name="look_up_values",
                                         index_col=0,
                                         dtype=str)

    value_dictionary = df_lookup_values.to_dict('index')
    main_values_list = df_main_values["Main values"].tolist()

    new_df_dict = {
        "Main values": [],
        "value 1": [],
        "value 2": [],
        "value 3": [],
        "value 4": [],
        "value 5": []
    }

    new_df = pd.DataFrame(new_df_dict)

    for main_value in main_values_list:
        if main_value in value_dictionary.keys():
            new_df.loc[len(new_df.index)] = [main_value, value_dictionary[main_value]["value 1"],
                                             value_dictionary[main_value]["value 2"],
                                             value_dictionary[main_value]["value 3"],
                                             value_dictionary[main_value]["value 4"],
                                             value_dictionary[main_value]["value 5"]]
        else:
            new_df.loc[len(new_df.index)] = [main_value, "", "", "", "", ""]

    new_df.fillna("", inplace=True)

    st.dataframe(new_df)

    st.download_button(
                label="Download result",
                data=to_excel(new_df),
                file_name='result.xlsx'
            )
