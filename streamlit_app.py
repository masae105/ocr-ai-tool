import os
import sys
import streamlit as st


sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)


from main import process_invoice
from excel import save_to_excel



st.title("OCR AI Tool")


st.write(
    "請求書・書類を自動解析するOCRツール"
)



uploaded_files = st.file_uploader(
    "ファイルを選択してください",
    accept_multiple_files=True,
    type=[
        "png",
        "jpg",
        "jpeg",
        "pdf"
    ]
)



if uploaded_files:


    st.success(
        f"{len(uploaded_files)}件読み込みました"
    )


    for uploaded_file in uploaded_files:

        st.image(
            uploaded_file,
            caption=uploaded_file.name
        )



    if st.button("解析開始"):


        results = []


        temp_dir = "temp"


        os.makedirs(
            temp_dir,
            exist_ok=True
        )



        for uploaded_file in uploaded_files:


            file_path = os.path.join(
                temp_dir,
                uploaded_file.name
            )



            with open(
                file_path,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )



            data = process_invoice(
                file_path
            )


            results.append(data)



        # =====================
        # 解析結果表示
        # =====================


        for data in results:


            st.subheader(
                "請求書解析結果"
            )


            st.write("会社名")

            st.write(
                data.get(
                    "会社名",
                    ""
                )
            )



            st.write("請求日")

            st.write(
                data.get(
                    "請求日",
                    ""
                )
            )



            st.write("合計金額")


            st.markdown(
                f"### {data.get('合計金額', 0):,} 円"
            )



            st.write("金額チェック")


            check = data.get(
                "金額チェック",
                ""
            )



            if check == "OK":

                st.write(
                    "OK"
                )

            else:

                st.error(
                    "⚠ 確認が必要です"
                )



            st.subheader(
                "商品明細"
            )



            details = [

                {
                    "商品名": item["商品名"],
                    "金額": item["金額"]
                }

                for item in data.get(
                    "明細",
                    []
                )

            ]



            st.dataframe(

                details,

                hide_index=True,

                use_container_width=True,

                column_config={

                    "商品名":
                    st.column_config.TextColumn(
                        "商品名"
                    ),


                    "金額":
                    st.column_config.NumberColumn(
                        "金額",
                        format="%d 円"
                    )

                }

            )


            st.divider()



        # =====================
        # Excel出力
        # =====================


        output_path = (
            "output/result.xlsx"
        )

        st.write(results)
        save_to_excel(

            results,

            output_path

        )



        with open(

            output_path,

            "rb"

        ) as file:


            st.download_button(

                label="Excelダウンロード",

                data=file,

                file_name="invoice_result.xlsx",

                mime=
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            )