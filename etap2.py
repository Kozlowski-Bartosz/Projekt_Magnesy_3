import numpy as np
import matplotlib.pyplot as plt

# Parametry sygnałów
amplituda = 1
A = 1
K = 1
t1 = 1
t2 = 1
n = 1
f = 1
fi = 0

# Inicjalizacja wykresów
fig, ax = plt.subplots()
fig2, axs2 = plt.subplots()

# Tworzenie wektora czasu
czas_trwania = 20
okres_probkowania = 0.01
czas = np.arange(0, czas_trwania, okres_probkowania)

# Inicjalizacja linii wykresów
linia1, = ax.plot(czas, np.zeros_like(czas))
linia2, = axs2.plot([], [])

# Konfiguracja wykresów
ax.set_title('Sygnał')
ax.set_xlabel('Czas [s]')
ax.set_ylabel('Amplituda')

axs2.set_title('Transformata Fouriera')
axs2.set_xlabel('Częstotliwość [Hz]')
axs2.set_ylabel('Amplituda')

polowa_indeksow = int(np.ceil(len(czas) / 2))

# Funkcja aktualizująca wykresy
def update():
    global A, K, t1, t2, n, f, fi

    sygnal = A * K * ((czas/t1)**n)/(1 + (czas/t1)**n) * np.exp(-czas/t2) * np.cos(2*np.pi*f*czas + fi)



    linia1.set_ydata(sygnal)
    ax.set_xlim([czas[0], czas[-1]])
    ax.set_ylim([-5.0, 5.0])

    widmo = np.abs(np.fft.fft(sygnal)[:polowa_indeksow])
    maksimum_widmo = np.max(widmo)

    linia2.set_data(np.fft.fftfreq(len(czas), okres_probkowania)[:polowa_indeksow], widmo)
    axs2.set_xlim(0, 10)
    axs2.set_ylim([np.min(widmo), maksimum_widmo if maksimum_widmo > 500 else 500])

    fig.canvas.draw_idle()
    fig2.canvas.draw_idle()

# Konfiguracja narzędzi interaktywnych
plt.subplots_adjust(bottom=0.5)
axcolor = 'lightgoldenrodyellow'
slider_A = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)
slider_K = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)
slider_t1 = plt.axes([0.15, 0.2, 0.7, 0.03], facecolor=axcolor)
slider_t2 = plt.axes([0.15, 0.25, 0.7, 0.03], facecolor=axcolor)
slider_n = plt.axes([0.15, 0.3, 0.7, 0.03], facecolor=axcolor)
slider_f = plt.axes([0.15, 0.35, 0.7, 0.03], facecolor=axcolor)
slider_fi = plt.axes([0.15, 0.4, 0.7, 0.03], facecolor=axcolor)

slider_A_obj = plt.Slider(slider_A, 'A', 0.1, 10.0, valinit=A, valstep=0.1)
slider_K_obj = plt.Slider(slider_K, 'K', 0.1, 10.0, valinit=K, valstep=0.1)
slider_t1_obj = plt.Slider(slider_t1, 't1', 0.1, czas_trwania, valinit=t1, valstep=0.1)
slider_t2_obj = plt.Slider(slider_t2, 't2', 0.1, czas_trwania, valinit=t2, valstep=0.1)
slider_n_obj = plt.Slider(slider_n, 'n', 0.1, 10.0, valinit=n, valstep=0.1)
slider_f_obj = plt.Slider(slider_f, 'f', 0.1, 10.0, valinit=f, valstep=0.1)
slider_fi_obj = plt.Slider(slider_fi, 'fi', 0.0, 2*np.pi, valinit=fi, valstep=0.1)

def update_params(val):
    global A, K, t1, t2, n, f, fi

    A = slider_A_obj.val
    K = slider_K_obj.val
    t1 = slider_t1_obj.val
    t2 = slider_t2_obj.val
    n = slider_n_obj.val
    f = slider_f_obj.val
    fi = slider_fi_obj.val

    update()

slider_A_obj.on_changed(update_params)
slider_K_obj.on_changed(update_params)
slider_t1_obj.on_changed(update_params)
slider_t2_obj.on_changed(update_params)
slider_n_obj.on_changed(update_params)
slider_f_obj.on_changed(update_params)
slider_fi_obj.on_changed(update_params)

# Wywołanie funkcji update dla inicjalizacji wykresów
update()

# Wyświetlanie okien graficznych
plt.show()
