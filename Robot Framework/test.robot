*** Settings ***
Library    helper.py
Library    SeleniumLibrary


*** Variables ***
${REPORT_FILE}=        file:///C:/Users/sofiia_ziniuk/Desktop/report.html
${PARQUET_FOLDER}=        C:\\Users\\sofiia_ziniuk\\Desktop\\parquet_data
${FILTER_DATE}=       2026-03


*** Test Cases ***
Comparing two DataFrames Test
    Open Browser    ${REPORT_FILE}    Chrome
    ${sl}=          Get Library Instance    SeleniumLibrary
    ${driver}=      Set Variable    ${sl.driver}
    ${html_table}=    Extract Table To Dataframe    ${driver}
    ${parquet_data}=   Read Parquet Dataset    ${PARQUET_FOLDER}
    ${filtered_html_table}=      Filter By Partition Date          ${parquet_data}    ${FILTER_DATE}
    ${comparison}=    Compare Dataframes    ${filtered_html_table}    ${parquet_data}
    Should Be True      ${comparison["values_equal"]}    \nDATAFRAMES DO NOT MATCH:\n${comparison["value_diff"]}




