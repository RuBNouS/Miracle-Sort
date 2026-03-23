import customtkinter as ctk #interface
import random #gerar números aleatórios
import webbrowser #abrir links
import os #desligar o PC (esta comentado)
import platform

class InterfaceMiracleSort(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #nome e tamanho da janela
        self.title("Miracle Sort")
        self.geometry("500x300")
        
        #variáveis
        self.array = []
        self.sorting = False #indica se o miracle sort está a correr
        self.posição_verificação = 0 #guarda a posição atual da verificação
        self.check_loop = None
        self.evento_ativo = False #pausa a animação de texto durante eventos
        
        #interface array
        self.array_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.array_frame.pack(pady=(15, 5))
        self.lista = [] 
        
        for _ in range(5):
            lbl = ctk.CTkLabel(self.array_frame, text="[--]", font=ctk.CTkFont(size=24, family="Courier"))
            lbl.pack(side="left", padx=5)
            self.lista.append(lbl)
        
        #interface status e botões
        self.texto_estado = ctk.CTkLabel(self, text="Gere uma lista para começar.", font=ctk.CTkFont(size=14))
        self.texto_estado.pack(pady=15)
        
        self.bt_GerarLista = ctk.CTkButton(self, text="Gerar Lista (5 números)", command=self.generate_array, width=300)
        self.bt_GerarLista.pack(pady=(5, 5))
        
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=5)

        self.bt_Iniciar = ctk.CTkButton(self.btn_frame, text="Iniciar Miracle Sort", command=self.start_miracle_sort, state="disabled", width=145, fg_color="#2E8B57", hover_color="#236B43")
        self.bt_Iniciar.pack(side="left", padx=5)

        self.bt_Parar = ctk.CTkButton(self.btn_frame, text="Parar Miracle Sort", command=self.stop_miracle_sort, state="disabled", width=145, fg_color="#C62828", hover_color="#8F1D1D")
        self.bt_Parar.pack(side="right", padx=5)
        
        self.bt_CosmicRay = ctk.CTkButton(self, text="Forçar Cosmic Ray", command=self.force_cosmic_ray, width=300, fg_color="#673AB7", hover_color="#512DA8")
        self.bt_CosmicRay.pack(pady=20)

    #desligar/ligar botões se o miracle sort estiver a correr ou não
    def set_buttons_state(self, sorting):
        self.bt_Iniciar.configure(state="disabled" if sorting else "normal")
        self.bt_Parar.configure(state="normal" if sorting else "disabled")

    #desligar todos os botões (quando sai desligar pc/fechar app)
    def disable_all_buttons(self):
        self.bt_GerarLista.configure(state="disabled")
        self.bt_Iniciar.configure(state="disabled")
        self.bt_Parar.configure(state="disabled")
        self.bt_CosmicRay.configure(state="disabled")

    #gera 5 números (0 a 99), atualiza a interface e permite iniciar o miracle sort
    def generate_array(self):
        self.stop_miracle_sort() 
        self.array = [random.randint(0, 99) for _ in range(5)]
        self.update_array_display()
        self.texto_estado.configure(text="Lista gerada.", text_color="white")
        self.set_buttons_state(sorting=False)

    #lê a lista gerada e atualiza a interface (usada após cosmic ray alterar a lista)
    def update_array_display(self):
        for i, num in enumerate(self.array):
            self.lista[i].configure(text=f"[{num}]", text_color="white")

    #inicia o miracle sort, animação de texto e o ciclo de verificação
    def start_miracle_sort(self):
        self.sorting = True
        self.set_buttons_state(sorting=True)
        self.animate_status_text(0) 
        self.start_verification_cycle() 

    #para o miracle sort, animação e ciclo de verificação
    def stop_miracle_sort(self):
        self.sorting = False
        
        if self.check_loop:
            self.after_cancel(self.check_loop)
            self.check_loop = None

        if self.array:
            self.set_buttons_state(sorting=False)
            
        self.texto_estado.configure(text="Verificação parada.", text_color="white")
        
        for lbl in self.lista:
            lbl.configure(text_color="white")

    #garante que o programa cancela uma espera anterior antes de começar uma nova (animação e o ciclo de verificação)
    def schedule_next_step(self, delay, function_to_call):
        if self.check_loop:
            self.after_cancel(self.check_loop)
        self.check_loop = self.after(delay, function_to_call)

    #animação de texto dos ... 
    def animate_status_text(self, count):
        if not self.sorting:
            return 

        try:
            #só atualiza a animação dos pontinhos se não houver um evento ativo
            if not self.evento_ativo:
                dots = "." * (count % 4)
                self.texto_estado.configure(text=f"À espera de um milagre{dots}")
            self.after(500, self.animate_status_text, count + 1)
        except ctk.TclError:
            pass #ignora erro se a janela for fechada durante a animação

    #ciclo de verificação do miracle sort. pinta o 1º de verde e compara dps de 300ms
    def start_verification_cycle(self):
        if not self.sorting:
            return
            
        for lbl in self.lista:
            lbl.configure(text_color="white")
        
        self.lista[0].configure(text_color="lightgreen")
        self.posição_verificação = 0
        self.schedule_next_step(300, self.check_step)

    #verifica se o array está ordenado.
    def check_step(self):
        if not self.sorting:
            return
        #se chegou ao fim da lista, o milagre aconteceu
        if self.posição_verificação >= len(self.array) - 1:
            self.texto_estado.configure(text="A lista está ordenada! O milagre aconteceu!", text_color="lightgreen")
            self.sorting = False
            self.set_buttons_state(sorting=False)
            return

        #compara o valor atual com o próximo e pinta de verde se estiver correto ou vermelho se não estiver. Depois de 800ms recomeça
        val_current = self.array[self.posição_verificação]
        val_next = self.array[self.posição_verificação + 1]

        if val_current <= val_next:
            self.lista[self.posição_verificação + 1].configure(text_color="lightgreen")
            self.posição_verificação += 1
            self.schedule_next_step(300, self.check_step)
        else:
            self.lista[self.posição_verificação  + 1].configure(text_color="red")
            self.schedule_next_step(800, self.start_verification_cycle)

    #reseta as animações dps de um cosmic ray
    def reset_event_status(self):
        self.evento_ativo = False
        if self.sorting:
            self.texto_estado.configure(text_color="white")

    #evento cosmic ray
    def force_cosmic_ray(self):
        if not self.array:
            return
            
        chance = random.randint(1, 100)
        self.evento_ativo = True # Pausa animação
        
        #fechar aplicação
        if chance <= 5: #5% chance
            self.stop_miracle_sort()
            self.disable_all_buttons()
            self.texto_estado.configure(text="Erro Crítico: A app vai fechar...", text_color="red")
            self.after(1500, self.destroy)
        
        #desligar PC (comentado porque né lol)
        elif chance <= 10: #5% de chance
            self.stop_miracle_sort()
            self.disable_all_buttons()
            self.texto_estado.configure(text="Erro Mega Crítico: A desligar o sistema...", text_color="red")
            
            # if platform.system() == "Windows":
            #     os.system("shutdown /s /t 5")
            # else:
            #     os.system("shutdown now")
            
            self.after(2000, self.destroy)
        
        #rick roll
        elif chance <= 20: #10% de chance
            self.texto_estado.configure(text="Never gonna give you up...", text_color="#D35400") #"dourado anos 80"
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            self.after(2500, self.reset_event_status)
        
        #github
        elif chance <= 30: #10% de chance
            self.texto_estado.configure(text="Erro: Redirecionando para documentação de emergência (GitHub)...", text_color="#673AB7")
            webbrowser.open("https://github.com/RuBNouS")
            self.after(2500, self.reset_event_status)
        
        #ideia do miracle sort default
        else: #70% de chance
            idx = random.randint(0, len(self.array) - 1)
            bit_to_flip = random.randint(0, 6) 
            
            self.array[idx] ^= (1 << bit_to_flip)
            self.update_array_display()
            self.texto_estado.configure(text="Radiação alterou a memória!", text_color="#00F2FF") #cor que supostamente nós associamos a um cosmic ray
            
            if self.sorting:
                self.schedule_next_step(800, self.start_verification_cycle)
            
            self.after(1500, self.reset_event_status)

if __name__ == "__main__":
    app = InterfaceMiracleSort()
    app.mainloop()
