import numpy as np
import matplotlib.pyplot as plt

# Parametry sygnałów
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
signal_time = 20
sampling_frequency = 0.01
time = np.arange(0, signal_time, sampling_frequency)

# Inicjalizacja linii wykresów
line_1, = ax.plot(time, np.zeros_like(time))
line_2, = axs2.plot([], [])

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
    global A, K, t1, t2, n, f, fi, signal_time, sampling_frequency, time
    
    time = np.arange(0, signal_time, sampling_frequency)

    sygnal = A * K * ((time/t1)**n)/(1 + (time/t1)**n) * np.exp(-time/t2) * np.cos(2*np.pi*f*time + fi)



    line_1.set_data(time, sygnal)
    ax.set_xlim([time[0], time[-1]])
    ax.set_ylim([-5.0, 5.0] if np.max(sygnal) < 5.0 else [np.min(sygnal), np.max(sygnal)])

    freq_spectrum = np.abs(np.fft.fft(sygnal)[:index_half])
    spectrum_max = np.max(freq_spectrum)

    line_2.set_data(np.fft.fftfreq(len(time), sampling_frequency)[:index_half], freq_spectrum)
    axs2.set_xlim(0, 10)
    axs2.set_ylim([np.min(freq_spectrum), spectrum_max if spectrum_max > 500 else 500])

    fig.canvas.draw_idle()
    fig2.canvas.draw_idle()

# Konfiguracja narzędzi interaktywnych
plt.subplots_adjust(bottom=0.5)
axcolor = 'lightgoldenrodyellow'
slider_signal_time = plt.axes([0.15, 0.4, 0.7, 0.03], facecolor=axcolor)
slider_sampling_frequency = plt.axes([0.15, 0.35, 0.7, 0.03], facecolor=axcolor)
slider_A = plt.axes([0.15, 0.3, 0.7, 0.03], facecolor=axcolor)
slider_K = plt.axes([0.15, 0.25, 0.7, 0.03], facecolor=axcolor)
slider_t1 = plt.axes([0.15, 0.2, 0.7, 0.03], facecolor=axcolor)
slider_t2 = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)
slider_n = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)
slider_f = plt.axes([0.15, 0.05, 0.7, 0.03], facecolor=axcolor)
slider_fi = plt.axes([0.15, 0.0, 0.7, 0.03], facecolor=axcolor)

slider_signal_time_obj = plt.Slider(slider_signal_time, 'Czas trwania', 1, 30, valinit=signal_time, valstep=1)
slider_sampling_frequency_obj = plt.Slider(slider_sampling_frequency, 'Okres próbkowania', 0.01, 1.0, valinit=sampling_frequency, valstep=0.01)
slider_A_obj = plt.Slider(slider_A, 'A', 0.01, 10.0, valinit=A, valstep=0.01)
slider_K_obj = plt.Slider(slider_K, 'K', 0.01, 10.0, valinit=K, valstep=0.01)
slider_t1_obj = plt.Slider(slider_t1, 't1', 0.001, signal_time, valinit=t1, valstep=0.001)
slider_t2_obj = plt.Slider(slider_t2, 't2', 0.001, signal_time, valinit=t2, valstep=0.001)
slider_n_obj = plt.Slider(slider_n, 'n', 0.01, 10.0, valinit=n, valstep=0.01)
slider_f_obj = plt.Slider(slider_f, 'f', 0.001, 10.0, valinit=f, valstep=0.001)
slider_fi_obj = plt.Slider(slider_fi, 'fi', 0.0, 2*np.pi, valinit=fi, valstep=0.01)

def update_params(val):
    global A, K, t1, t2, n, f, fi, signal_time, sampling_frequency

    A = slider_A_obj.val
    K = slider_K_obj.val
    t1 = slider_t1_obj.val
    t2 = slider_t2_obj.val
    n = slider_n_obj.val
    f = slider_f_obj.val
    fi = slider_fi_obj.val
    signal_time = slider_signal_time_obj.val
    sampling_frequency = slider_sampling_frequency_obj.val

    update()

slider_A_obj.on_changed(update_params)
slider_K_obj.on_changed(update_params)
slider_t1_obj.on_changed(update_params)
slider_t2_obj.on_changed(update_params)
slider_n_obj.on_changed(update_params)
slider_f_obj.on_changed(update_params)
slider_fi_obj.on_changed(update_params)
slider_signal_time_obj.on_changed(update_params)
slider_sampling_frequency_obj.on_changed(update_params)

# Wywołanie funkcji update dla inicjalizacji wykresów
update()

# Wyświetlanie okien graficznych
plt.show()
