import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(layout="wide")

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
            new_df.loc[len(new_df.index)] = [main_value,
                                             value_dictionary[main_value]["value 1"],
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


def create_graphs(answers, percents=True):
    df_q_5_1 = pd.DataFrame()
    df_q_5_1["Vecums"] = df_anketa["1) Jūsu vecums"]

    one_hot = pd.get_dummies(
        df_anketa[answers])
    df_q_5_1 = df_q_5_1.join(one_hot)

    st.title(answers)

    grouped_data = df_q_5_1.groupby("Vecums").sum()

    if not percents:
        st.subheader("Vērtibas gabalos")
        st.dataframe(grouped_data)

        st.line_chart(df_q_5_1.groupby("Vecums").sum())
        st.bar_chart(df_q_5_1.groupby("Vecums").sum())

    if percents:
        col_sum = grouped_data.sum(axis=1)
        df_percent = grouped_data.apply(lambda x: x / col_sum * 100, axis=0)

        st.subheader("Vērtibas procentos")
        st.dataframe(df_percent)

        st.line_chart(df_percent.groupby("Vecums").sum())
        st.bar_chart(df_percent.groupby("Vecums").sum())


with st.expander("ANKETA"):
    uploaded_anketa = st.file_uploader("Ieliec exceli", type=["csv", "xlsx"])

    values_for_tables = st.radio(
        "Vērtības procentos vai gabalos",
        ('Procentos', 'Gabalos'))

    df_anketa = pd.DataFrame()

    if uploaded_anketa is not None:
        print("bbb")
        if uploaded_anketa.type == "text/csv":
            df_anketa = pd.read_excel(uploaded_anketa, sheet_name="main")
        else:
            df_anketa = pd.read_excel(uploaded_anketa, sheet_name="main")

        values_for_tables_bool = True
        if values_for_tables == "Gabalos":
            values_for_tables_bool = False

        for current_answer in df_anketa.columns[2:]:
            create_graphs(answers=current_answer,
                          percents=values_for_tables_bool)
