import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime

class BansosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pembagian Bansos")
        self.root.geometry("800x600")
        
        # URL API
        self.base_url = "http://localhost:5000/api"
        
        # Membuat frame utama
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Form input
        ttk.Label(self.main_frame, text="NIK:").grid(row=0, column=0, sticky=tk.W)
        self.nik_var = tk.StringVar()
        self.nik_entry = ttk.Entry(self.main_frame, textvariable=self.nik_var)
        self.nik_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(self.main_frame, text="Nama:").grid(row=1, column=0, sticky=tk.W)
        self.nama_var = tk.StringVar()
        self.nama_entry = ttk.Entry(self.main_frame, textvariable=self.nama_var)
        self.nama_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(self.main_frame, text="Alamat:").grid(row=2, column=0, sticky=tk.W)
        self.alamat_var = tk.StringVar()
        self.alamat_entry = ttk.Entry(self.main_frame, textvariable=self.alamat_var)
        self.alamat_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(self.main_frame, text="Jenis Bansos:").grid(row=3, column=0, sticky=tk.W)
        self.jenis_bansos_var = tk.StringVar()
        self.jenis_bansos_combo = ttk.Combobox(self.main_frame, textvariable=self.jenis_bansos_var)
        self.jenis_bansos_combo['values'] = ('BLT', 'PKH', 'BPNT', 'BST')
        self.jenis_bansos_combo.grid(row=3, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(self.main_frame, text="Status:").grid(row=4, column=0, sticky=tk.W)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(self.main_frame, textvariable=self.status_var)
        self.status_combo['values'] = ('Belum Disalurkan', 'Sudah Disalurkan')
        self.status_combo.grid(row=4, column=1, sticky=(tk.W, tk.E))
        
        # Tombol CRUD
        ttk.Button(self.main_frame, text="Tambah", command=self.add_data).grid(row=5, column=0, pady=5)
        ttk.Button(self.main_frame, text="Update", command=self.update_data).grid(row=5, column=1, pady=5)
        ttk.Button(self.main_frame, text="Hapus", command=self.delete_data).grid(row=5, column=2, pady=5)
        
        # Treeview untuk menampilkan data
        self.tree = ttk.Treeview(self.main_frame, columns=('ID', 'NIK', 'Nama', 'Alamat', 'Jenis Bansos', 'Tanggal', 'Status'), show='headings')
        
        # Mengatur heading kolom
        self.tree.heading('ID', text='ID')
        self.tree.heading('NIK', text='NIK')
        self.tree.heading('Nama', text='Nama')
        self.tree.heading('Alamat', text='Alamat')
        self.tree.heading('Jenis Bansos', text='Jenis Bansos')
        self.tree.heading('Tanggal', text='Tanggal Terima')
        self.tree.heading('Status', text='Status')
        
        # Mengatur lebar kolom
        self.tree.column('ID', width=50)
        self.tree.column('NIK', width=100)
        self.tree.column('Nama', width=150)
        self.tree.column('Alamat', width=200)
        self.tree.column('Jenis Bansos', width=100)
        self.tree.column('Tanggal', width=100)
        self.tree.column('Status', width=100)
        
        self.tree.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        # Load data saat pertama kali
        self.load_data()
    
    def load_data(self):
        try:
            response = requests.get(f"{self.base_url}/penerima")
            if response.status_code == 200:
                # Hapus data lama di treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Tambahkan data baru
                for item in response.json():
                    self.tree.insert('', 'end', values=(
                        item['id'],
                        item['nik'],
                        item['nama'],
                        item['alamat'],
                        item['jenis_bansos'],
                        item['tanggal_terima'],
                        item['status']
                    ))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Gagal mengambil data: {str(e)}")
    
    def add_data(self):
        data = {
            'nik': self.nik_var.get(),
            'nama': self.nama_var.get(),
            'alamat': self.alamat_var.get(),
            'jenis_bansos': self.jenis_bansos_var.get(),
            'status': self.status_var.get()
        }
        
        try:
            response = requests.post(f"{self.base_url}/penerima", json=data)
            if response.status_code == 201:
                messagebox.showinfo("Sukses", "Data berhasil ditambahkan")
                self.load_data()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Gagal menambahkan data")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {str(e)}")
    
    def update_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diupdate")
            return
        
        item_id = self.tree.item(selected_item[0])['values'][0]
        
        data = {
            'nik': self.nik_var.get(),
            'nama': self.nama_var.get(),
            'alamat': self.alamat_var.get(),
            'jenis_bansos': self.jenis_bansos_var.get(),
            'status': self.status_var.get()
        }
        
        try:
            response = requests.put(f"{self.base_url}/penerima/{item_id}", json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sukses", "Data berhasil diupdate")
                self.load_data()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Gagal mengupdate data")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Gagal mengupdate data: {str(e)}")
    
    def delete_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus")
            return
        
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            item_id = self.tree.item(selected_item[0])['values'][0]
            
            try:
                response = requests.delete(f"{self.base_url}/penerima/{item_id}")
                if response.status_code == 200:
                    messagebox.showinfo("Sukses", "Data berhasil dihapus")
                    self.load_data()
                    self.clear_form()
                else:
                    messagebox.showerror("Error", "Gagal menghapus data")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {str(e)}")
    
    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            self.nik_var.set(values[1])
            self.nama_var.set(values[2])
            self.alamat_var.set(values[3])
            self.jenis_bansos_var.set(values[4])
            self.status_var.set(values[6])
    
    def clear_form(self):
        self.nik_var.set('')
        self.nama_var.set('')
        self.alamat_var.set('')
        self.jenis_bansos_var.set('')
        self.status_var.set('')

if __name__ == '__main__':
    root = tk.Tk()
    app = BansosApp(root)
    root.mainloop()