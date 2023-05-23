import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, RadioButtons

# Parametry sygnałów
A1 = 1
f1 = 1
fi1 = 0
A2 = 0.5
f2 = 2
fi2 = np.pi/4

# Inicjalizacja wykresów
fig, ax = plt.subplots()
fig2, axs2 = plt.subplots()

# Tworzenie wektora czasu
czas_trwania = 20
okres_probkowania = 0.01
czas = np.arange(0, czas_trwania, okres_probkowania)
window = np.ones(len(czas))

# Inicjalizacja linii wykresów
linia1, = ax.plot(czas, np.zeros_like(czas), label='Sygnał 1')
linia2, = ax.plot(czas, np.zeros_like(czas), label='Sygnał 2')
linia3, = ax.plot(czas, np.zeros_like(czas), label='Sygnał Złożony')
linia4, = axs2.plot([], [])

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
    global A1, f1, fi1, A2, f2, fi2, czas_trwania, okres_probkowania, czas, window
    
    czas = np.arange(0, czas_trwania, okres_probkowania)
    update_window(buttons_window_obj.value_selected)

    # Sygnały sinusoidalne
    sygnal1 = A1 * np.sin(2 * np.pi * f1 * czas + fi1) * window
    sygnal2 = A2 * np.sin(2 * np.pi * f2 * czas + fi2) * window
    sygnal = sygnal1 + sygnal2
    
    linia1.set_data(czas, sygnal1)
    linia2.set_data(czas, sygnal2)
    linia3.set_data(czas, sygnal)
    ax.set_xlim([czas[0], czas[-1]])
    ax.set_ylim([-5.0, 5.0])

    widmo = np.abs(np.fft.fft(sygnal)[:polowa_indeksow])
    maksimum_widmo = np.max(widmo)

    linia4.set_data(np.fft.fftfreq(len(czas), okres_probkowania)[:polowa_indeksow], widmo)
    axs2.set_xlim(0, 10)
    axs2.set_ylim([np.min(widmo), maksimum_widmo if maksimum_widmo > 500 else 500])

    fig.canvas.draw_idle()
    fig2.canvas.draw_idle()

# Konfiguracja narzędzi interaktywnych
plt.subplots_adjust(bottom=0.65)
axcolor = 'lightgoldenrodyellow'
buttons_window = plt.axes([0.65, 0.5, 0.3, 0.08])
buttons_signal = plt.axes([0.65, 0.4, 0.3, 0.08])
slider_czas_trwania = plt.axes([0.15, 0.45, 0.4, 0.03], facecolor=axcolor)
slider_okres_probkowania = plt.axes([0.15, 0.4, 0.4, 0.03], facecolor=axcolor)
slider_A1 = plt.axes([0.15, 0.35, 0.7, 0.03], facecolor=axcolor)
slider_f1 = plt.axes([0.15, 0.3, 0.7, 0.03], facecolor=axcolor)
slider_fi1 = plt.axes([0.15, 0.25, 0.7, 0.03], facecolor=axcolor)
slider_A2 = plt.axes([0.15, 0.2, 0.7, 0.03], facecolor=axcolor)
slider_f2 = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)
slider_fi2 = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)

buttons_window_obj = RadioButtons(buttons_window, ('Brak', 'Hamminga', 'Barletta', 'Blackmana'), active=0)
buttons_signal_obj = CheckButtons(buttons_signal, ('Sygnał 1', 'Sygnał 2', 'Sygnał Złożony'), (True, True, True))
slider_czas_trwania_obj = plt.Slider(slider_czas_trwania, 'Czas trwania', 1, 30, valinit=czas_trwania, valstep=1)
slider_okres_probkowania_obj = plt.Slider(slider_okres_probkowania, 'Okres próbkowania', 0.01, 1.0, valinit=okres_probkowania, valstep=0.01)
slider_A1_obj = plt.Slider(slider_A1, 'A1', 0.01, 3.0, valinit=A1, valstep=0.01)
slider_f1_obj = plt.Slider(slider_f1, 'f1', 0.001, 10.0, valinit=f1, valstep=0.001)
slider_fi1_obj = plt.Slider(slider_fi1, 'fi1', 0.0, 2*np.pi, valinit=fi1, valstep=0.01)
slider_A2_obj = plt.Slider(slider_A2, 'A2', 0.01, 3.0, valinit=A2, valstep=0.01)
slider_f2_obj = plt.Slider(slider_f2, 'f2', 0.001, 10.0, valinit=f2, valstep=0.001)
slider_fi2_obj = plt.Slider(slider_fi2, 'fi2', 0.0, 2*np.pi, valinit=fi2, valstep=0.01)

def update_params(val):
    global A1, f1, fi1, A2, f2, fi2, czas_trwania, okres_probkowania

    A1 = slider_A1_obj.val
    f1 = slider_f1_obj.val
    fi1 = slider_fi1_obj.val
    A2 = slider_A2_obj.val
    f2 = slider_f2_obj.val
    fi2 = slider_fi2_obj.val
    czas_trwania = slider_czas_trwania_obj.val
    okres_probkowania = slider_okres_probkowania_obj.val

    update()
    
def update_window(label = ""):
    global czas, window

    if label == 'Hamminga':
        window = np.hamming(len(czas))
    elif label == 'Barletta':
        window = np.bartlett(len(czas))
    elif label == 'Blackmana':
        window = np.blackman(len(czas))
    else:
        window = np.ones(len(czas))
        
    return window

buttons_window_obj.on_clicked(update_params)
slider_A1_obj.on_changed(update_params)
slider_f1_obj.on_changed(update_params)
slider_fi1_obj.on_changed(update_params)
slider_A2_obj.on_changed(update_params)
slider_f2_obj.on_changed(update_params)
slider_fi2_obj.on_changed(update_params)
slider_czas_trwania_obj.on_changed(update_params)
slider_okres_probkowania_obj.on_changed(update_params)


def toggle_visibility(label):
    if label == 'Sygnał 1':
        linia1.set_visible(not linia1.get_visible())
    elif label == 'Sygnał 2':
        linia2.set_visible(not linia2.get_visible())
    elif label == 'Sygnał Złożony':
        linia3.set_visible(not linia3.get_visible())

    fig.canvas.draw_idle()

buttons_signal_obj.on_clicked(toggle_visibility)

# Wywołanie funkcji update dla inicjalizacji wykresów
update()

# Wyświetlanie okien graficznych
plt.show()
