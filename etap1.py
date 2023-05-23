import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, RadioButtons

# Parametry sygnałów
A1 = 1
f1 = 4.35
fi1 = 0
A2 = 0.5
f2 = 8.7
fi2 = np.pi/4

# Inicjalizacja wykresów
fig, ax = plt.subplots()
fig2, axs2 = plt.subplots()

# Tworzenie wektora czasu
signal_time = 30
sampling_frequency = 0.01
time = np.arange(0, signal_time, sampling_frequency)
window = np.ones(len(time))

# Inicjalizacja linii wykresów
line_1, = ax.plot(time, np.zeros_like(time), label='Sygnał 1')
line_2, = ax.plot(time, np.zeros_like(time), label='Sygnał 2')
line_3, = ax.plot(time, np.zeros_like(time), label='Sygnał Złożony')
line_4, = axs2.plot([], [])

# Konfiguracja wykresów
ax.set_title('Sygnał')
ax.set_xlabel('Czas [s]')
ax.set_ylabel('Amplituda')

axs2.set_title('Transformata Fouriera')
axs2.set_xlabel('Częstotliwość [Hz]')
axs2.set_ylabel('Amplituda')

index_half = int(np.ceil(len(time) / 2))

# Funkcja aktualizująca wykresy
def update():
    global A1, f1, fi1, A2, f2, fi2, signal_time, sampling_frequency, time, window
    
    
    
    time = np.arange(0, signal_time, sampling_frequency)
    
    update_window(buttons_window_obj.value_selected)

    # Sygnały sinusoidalne
    signal1 = A1 * np.sin(2 * np.pi * f1 * time + fi1) * window
    signal2 = A2 * np.sin(2 * np.pi * f2 * time + fi2) * window
    signal_combined = signal1 + signal2
    
    line_1.set_data(time, signal1)
    line_2.set_data(time, signal2)
    line_3.set_data(time, signal_combined)
    ax.set_xlim([time[0], time[-1]])
    ax.set_ylim([-5.0, 5.0])

    fourier = np.abs(np.fft.fft(signal_combined)[:index_half])
    spectrum_max = np.max(fourier)

    line_4.set_data(np.fft.fftfreq(len(time), sampling_frequency)[:index_half], fourier)
    axs2.set_xlim(0, 10)
    axs2.set_ylim([np.min(fourier), spectrum_max if spectrum_max > 500 else 500])

    fig.canvas.draw_idle()
    fig2.canvas.draw_idle()

# Konfiguracja narzędzi interaktywnych
plt.subplots_adjust(bottom=0.65)
axcolor = 'lightgoldenrodyellow'
buttons_window = plt.axes([0.65, 0.5, 0.3, 0.08])
buttons_signal = plt.axes([0.65, 0.4, 0.3, 0.08])
slider_signal_time = plt.axes([0.15, 0.45, 0.4, 0.03], facecolor=axcolor)
slider_sampling_frequency = plt.axes([0.15, 0.4, 0.4, 0.03], facecolor=axcolor)
slider_A1 = plt.axes([0.15, 0.35, 0.7, 0.03], facecolor=axcolor)
slider_f1 = plt.axes([0.15, 0.3, 0.7, 0.03], facecolor=axcolor)
slider_fi1 = plt.axes([0.15, 0.25, 0.7, 0.03], facecolor=axcolor)
slider_A2 = plt.axes([0.15, 0.2, 0.7, 0.03], facecolor=axcolor)
slider_f2 = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)
slider_fi2 = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)

buttons_window_obj = RadioButtons(buttons_window, ('Brak', 'Hamminga', 'Barletta', 'Blackmana'), active=0)
buttons_signal_obj = CheckButtons(buttons_signal, ('Sygnał 1', 'Sygnał 2', 'Sygnał Złożony'), (True, True, True))
slider_signal_time_obj = plt.Slider(slider_signal_time, 'Czas trwania', 1, 30, valinit=signal_time, valstep=1)
slider_sampling_frequency_obj = plt.Slider(slider_sampling_frequency, 'Okres próbkowania', 0.01, 1.0, valinit=sampling_frequency, valstep=0.01)
slider_A1_obj = plt.Slider(slider_A1, 'A1', 0.01, 3.0, valinit=A1, valstep=0.01)
slider_f1_obj = plt.Slider(slider_f1, 'f1', 0.001, 10.0, valinit=f1, valstep=0.001)
slider_fi1_obj = plt.Slider(slider_fi1, 'fi1', 0.0, 2*np.pi, valinit=fi1, valstep=0.01)
slider_A2_obj = plt.Slider(slider_A2, 'A2', 0.01, 3.0, valinit=A2, valstep=0.01)
slider_f2_obj = plt.Slider(slider_f2, 'f2', 0.001, 10.0, valinit=f2, valstep=0.001)
slider_fi2_obj = plt.Slider(slider_fi2, 'fi2', 0.0, 2*np.pi, valinit=fi2, valstep=0.01)

def update_params(val):
    global A1, f1, fi1, A2, f2, fi2, signal_time, sampling_frequency

    A1 = slider_A1_obj.val
    f1 = slider_f1_obj.val
    fi1 = slider_fi1_obj.val
    A2 = slider_A2_obj.val
    f2 = slider_f2_obj.val
    fi2 = slider_fi2_obj.val
    signal_time = slider_signal_time_obj.val
    sampling_frequency = slider_sampling_frequency_obj.val

    update()
    
def update_window(label = ""):
    global time, window

    if label == 'Hamminga':
        window = np.hamming(len(time))
    elif label == 'Barletta':
        window = np.bartlett(len(time))
    elif label == 'Blackmana':
        window = np.blackman(len(time))
    else:
        window = np.ones(len(time))
        
    return window

buttons_window_obj.on_clicked(update_params)
slider_A1_obj.on_changed(update_params)
slider_f1_obj.on_changed(update_params)
slider_fi1_obj.on_changed(update_params)
slider_A2_obj.on_changed(update_params)
slider_f2_obj.on_changed(update_params)
slider_fi2_obj.on_changed(update_params)
slider_signal_time_obj.on_changed(update_params)
slider_sampling_frequency_obj.on_changed(update_params)


def toggle_visibility(label):
    if label == 'Sygnał 1':
        line_1.set_visible(not line_1.get_visible())
    elif label == 'Sygnał 2':
        line_2.set_visible(not line_2.get_visible())
    elif label == 'Sygnał Złożony':
        line_3.set_visible(not line_3.get_visible())

    fig.canvas.draw_idle()

buttons_signal_obj.on_clicked(toggle_visibility)

# Wywołanie funkcji update dla inicjalizacji wykresów
update()

# Wyświetlanie okien graficznych
plt.show()
