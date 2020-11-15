from cx_Freeze import setup,Executable

executables = [Executable("main.py")]

build_exe_options = {"packages": ["pygame",'random'],"include_files": ['apple.png','apple_bite.wav','Arizona-Sunset.mp3','food.py','high_scores.txt','Retro_No hope.ogg','score.py','snake.py','trophy.png','vgdeathsound.ogg']}


setup(
        name = 'Snake',
        options={'build_exe': build_exe_options},
        executables=executables)


        

