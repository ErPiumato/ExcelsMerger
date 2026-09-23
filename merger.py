import polars as pl

EXCEL1_PATH = "excelIn/ex1.xlsx"
EXCEL1_SHEET = ""
EXCEL1_COL = "ID"

EXCEL2_PATH = "excelIn/ex2.xlsx"
EXCEL2_SHEET = ""
EXCEL2_COL = "ID"

EXCEL_OUT_PATH = "excelOut/merged.xlsx"
if EXCEL1_SHEET != "":
    df1 = pl.read_excel(EXCEL1_PATH, sheet_name=EXCEL1_SHEET, engine="openpyxl")
else:
    df1 = pl.read_excel(EXCEL1_PATH, engine="openpyxl")
    
if EXCEL2_SHEET != "":
    df2 = pl.read_excel(EXCEL2_PATH, sheet_name=EXCEL2_SHEET, engine="openpyxl")
else:
    df2 = pl.read_excel(EXCEL2_PATH, engine="openpyxl")

if EXCEL1_COL not in df1.columns:
    raise ValueError(
        f"Colonna '{EXCEL1_COL}' non trovata nel primo file. "
        f"Colonne disponibili: {df1.columns}"
    )
if EXCEL2_COL not in df2.columns:
    raise ValueError(
        f"Colonna '{EXCEL2_COL}' non trovata nel secondo file. "
        f"Colonne disponibili: {df2.columns}"
    )

df1 = df1.with_columns(
    pl.col(EXCEL1_COL).cast(pl.Utf8).str.strip_chars().str.to_uppercase()
)
df2 = df2.with_columns(
    pl.col(EXCEL2_COL).cast(pl.Utf8).str.strip_chars().str.to_uppercase()
)

result = df1.join(
    df2,
    left_on=EXCEL1_COL,
    right_on=EXCEL2_COL,
    how="left",
    suffix="_file2",
)

colonne_solo_file2 = [c for c in df2.columns if c != EXCEL2_COL]
if colonne_solo_file2:
    indicatore = colonne_solo_file2[0]
    nome_colonna_indicatore = (
        f"{indicatore}_file2" if indicatore in df1.columns else indicatore
    )
    trovati = result[nome_colonna_indicatore].is_not_null().sum()
else:
    trovati = 0

print(f"Righe totali (dal primo file): {result.height}")
print(f"Di cui con corrispondenza trovata nel secondo file: {trovati}")

result.write_excel(EXCEL_OUT_PATH)
print(f"File creato: {EXCEL_OUT_PATH}")