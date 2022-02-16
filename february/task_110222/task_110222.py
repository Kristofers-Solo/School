# Author - Kristiāns Francis Cagulis
# Date - 11.02.2022
# Title - Classwork PDF

from fpdf import FPDF
import pandas as pd

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
print("Width: ", pdf.w)
print("Margins: ", pdf.l_margin)
usable_w = pdf.w - 2 * pdf.l_margin
print("Really usable: ", usable_w)

dislike = ["N/A", "NA", "--"]
data = pd.read_csv("auto_imports_mainits.csv", na_values=dislike)
del data["normalized-losses"]

select_data = data[["make", "engine-size", "num-of-doors"]]
select_data = select_data.sort_values(by=["make", "engine-size", "num-of-doors"])
select_data = select_data.drop_duplicates()

col_width = usable_w / 3
height = pdf.font_size * 2

for i in range(select_data.shape[0]):
	pdf.cell(col_width, height, str(select_data["make"].iloc[i]), border=1)
	pdf.cell(col_width, height, str(select_data["engine-size"].iloc[i]), border=1)
	pdf.cell(col_width, height, str(select_data["num-of-doors"].iloc[i]), border=1)
	pdf.ln(height)

# pdf.image("output.png", x=None, y=None, w=usable_w, h=0)
pdf.output("output.pdf")