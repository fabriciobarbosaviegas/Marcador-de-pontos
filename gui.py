import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys

from main import process_file


class GeocodeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Marcador de Pontos - GUI')
        self.geometry('640x360')

        self.file_path_var = tk.StringVar()
        self.output_var = tk.StringVar(value='enderecos_com_coordenadas.csv')

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(padx=12, pady=12, fill='x')

        tk.Label(frame, text='Arquivo ODS:').grid(row=0, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.file_path_var, width=60).grid(row=0, column=1, padx=6)
        tk.Button(frame, text='Selecionar', command=self.select_file).grid(row=0, column=2)

        tk.Label(frame, text='Arquivo de saída:').grid(row=1, column=0, sticky='w', pady=(8,0))
        tk.Entry(frame, textvariable=self.output_var, width=60).grid(row=1, column=1, padx=6, pady=(8,0))

        btn_frame = tk.Frame(self)
        btn_frame.pack(padx=12, pady=(6,0), fill='x')
        self.start_btn = tk.Button(btn_frame, text='Iniciar', command=self.start_processing)
        self.start_btn.pack(side='left')

        self.open_btn = tk.Button(btn_frame, text='Abrir CSV', command=self.open_output, state='disabled')
        self.open_btn.pack(side='left', padx=6)

        self.progress = scrolledtext.ScrolledText(self, height=12)
        self.progress.pack(padx=12, pady=12, fill='both', expand=True)

    def select_file(self):
        path = filedialog.askopenfilename(title='Selecione o arquivo .ods', filetypes=[('ODS files', '*.ods'), ('All files', '*.*')])
        if path:
            self.file_path_var.set(path)

    def log(self, msg: str):
        self.progress.insert('end', msg + '\n')
        self.progress.see('end')

    def start_processing(self):
        file_path = self.file_path_var.get()
        output = self.output_var.get()
        if not file_path:
            messagebox.showwarning('Aviso', 'Selecione um arquivo ODS antes de iniciar.')
            return

        # Desabilita botões enquanto processa
        self.start_btn.config(state='disabled')
        self.open_btn.config(state='disabled')
        self.progress.delete('1.0', 'end')
        self.log(f'Iniciando processamento: {file_path}')

        thread = threading.Thread(target=self._run_process, args=(file_path, output), daemon=True)
        thread.start()

    def _run_process(self, file_path, output):
        try:
            result_file, errors = process_file(file_path, output)
            self.log(f'Processamento finalizado. Arquivo: {result_file} | Erros: {errors}')
            self.open_btn.config(state='normal')
            messagebox.showinfo('Concluído', f'Arquivo gerado: {result_file}\nErros: {errors}')
        except Exception as e:
            self.log(f'Erro durante processamento: {e}')
            messagebox.showerror('Erro', f'Erro durante processamento:\n{e}')
        finally:
            self.start_btn.config(state='normal')

    def open_output(self):
        out = self.output_var.get()
        if os.path.exists(out):
            try:
                if sys.platform.startswith('win'):
                    os.startfile(os.path.abspath(out))
                else:
                    # Fallback para outros sistemas
                    os.system(f'xdg-open "{out}"')
            except Exception as e:
                messagebox.showerror('Erro', f'Não foi possível abrir o arquivo: {e}')
        else:
            messagebox.showwarning('Aviso', 'Arquivo de saída não encontrado.')


def main():
    app = GeocodeGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
