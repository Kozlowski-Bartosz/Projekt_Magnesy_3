import numpy as np
import matplotlib.pyplot as plt

# Parametry sygnałów
amplituda = 1              # Amplituda sygnałów
czestotliwosc1 = 1         # Częstotliwość pierwszego sygnału
czestotliwosc2 = 2         # Częstotliwość drugiego sygnału
czas_trwania = 4           # Czas trwania sygnału w sekundach
okres_probkowania = 0.01   # Okres próbkowania sygnału

# Tworzenie wektora czasu
czas = np.arange(0, czas_trwania, okres_probkowania)

# Sygnał sinusoidalny
sygnal_sinusoidalny = amplituda * np.sin(2 * np.pi * czestotliwosc1 * czas)

# Sygnał złożony z dwóch sinusoid
sygnal_zlozony = amplituda * (np.sin(2 * np.pi * czestotliwosc1 * czas) + np.sin(2 * np.pi * czestotliwosc2 * czas))

# Wyświetlanie sygnałów w dziedzinie czasu
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(czas, sygnal_sinusoidalny)
plt.title('Sygnał sinusoidalny')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')

plt.subplot(2, 1, 2)
plt.plot(czas, sygnal_zlozony)
plt.title('Sygnał złożony')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')

# Transformata Fouriera
czestotliwosc_probkowania = 1 / okres_probkowania
sygnal_sinusoidalny_fft = np.fft.fft(sygnal_sinusoidalny)
sygnal_zlozony_fft = np.fft.fft(sygnal_zlozony)

# Wartości częstotliwości dla osi częstotliwościowej
czestotliwosc = np.linspace(0, czestotliwosc_probkowania, len(czas))

# Ograniczenie wyników do prawostronnej połowy
polowa_indeksow = len(czestotliwosc) // 2
czestotliwosc = czestotliwosc[:polowa_indeksow]
sygnal_sinusoidalny_fft = np.abs(sygnal_sinusoidalny_fft[:polowa_indeksow])
sygnal_zlozony_fft = np.abs(sygnal_zlozony_fft[:polowa_indeksow])

# Wyświetlanie sygnałów w dziedzinie częstotliwości
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(czestotliwosc, sygnal_sinusoidalny_fft)
plt.title('Transformata Fouriera sygnału sinusoidalnego')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')

plt.subplot(2, 1, 2)
plt.plot(czestotliwosc, sygnal_zlozony_fft)
plt.title('Transformata Fouriera sygnału złożonego')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')

plt.tight_layout()
plt.show()
