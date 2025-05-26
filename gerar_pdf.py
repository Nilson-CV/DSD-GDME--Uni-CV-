from fpdf import FPDF
import datetime

class PDFRelatorio(FPDF):
    def header(self):
        # Logo (substitua 'logo.png' se tiver)
        try:
            self.image("logo.png", 10, 8, 25)
        except:
            pass  # Se o logo não existir, ignora

        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Universidade de Cabo Verde", ln=True, align="C")
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório de Carga Horária de Professores", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def gerar_pdf_estilizado(df):
    pdf = PDFRelatorio(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    col_widths = {
        "Professor": 40,
        "Grau": 25,
        "Max": 20,
        "Atual": 20,
        "Disciplina": 40,
        "Curso": 40,
        "Tipo": 25
    }

    row_height = 8
    line_height = 8

    # Cabeçalhos
    pdf.set_fill_color(200, 200, 200)
    pdf.set_font("Arial", "B", 10)
    for col in df.columns:
        pdf.cell(col_widths[col], row_height, col, border=1, fill=True)
    pdf.ln()

    # Linhas de dados
    pdf.set_font("Arial", size=9)
    fill = False
    for row in df.itertuples(index=False):
        for i, val in enumerate(row):
            col_name = df.columns[i]
            pdf.cell(col_widths[col_name], row_height, str(val), border=1, fill=fill)
        pdf.ln()
        fill = not fill  # Alternar cores (zebra)

    # Rodapé com data
    pdf.ln(5)
    pdf.set_font("Arial", "I", 8)
    data_hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 10, f"Gerado em: {data_hoje}", 0, 0, "R")

    return pdf.output(dest="S").encode("latin1")