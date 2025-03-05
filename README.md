# Spectrum_genererator
Необхідні бібліотеки для роботи всіх програм:
Python (версія 3.8 або новіша)
tkinter — для графічного інтерфейсу
matplotlib — для побудови графіків
numpy — для роботи з масивами даних
scipy — для обробки сигналів
pandas  — для роботи з таблицями (CSV)
argparse  — для роботи з аргументами командного рядка
json (тільки для spectrum_simulator.py) — для роботи з JSON-файлам

Встановити ці біліотеки можна такою командою:
pip install numpy matplotlib scipy pandas argparse
Для MacOs vj можна скористатись:
pip3 install numpy matplotlib scipy pandas argparse
крім того, для роботи з MacOs, раджу скачати python через brew і встановлювати додатково tkinter через нього.
Оскільки встановлення біліотек не відбувається у звчиному терміналі, то працювати краще у штучно створеному серидовищі, команди наводжу нижче:
python3 -m venv myenv
source myenv/bin/activate
pip install --upgrade pip
pip install numpy matplotlib scipy pandas argparse

Особливості роботи програм :
  
Програми spectrum_simulator.py i spectrum_analisator.py (1 i 2)

Звязок між програмами 1 і 2:
Програми 1 і 2 повязані через файл output.csv, який генерується програмою 1 і використовується програмою 2 для аналізу спектру.
Проблеми з детектуванням піків:
Виникають певні недоліки з детектуваням піків, повязані з краєвим ефектом, коли піки можуть бути невірно визначені на краях спектру,
що може впливати на якість результатів аналізу.

