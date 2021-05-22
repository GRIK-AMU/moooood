from re import sub
import keyboard as kb
import npyscreen as nps
from time import sleep
from plyer import notification

EMO_SHORTCUTS = {}

class Menu(nps.NPSApp):
	def main(self):
		F  = nps.Form()

		F.add(nps.FixedText, value='Shortcut for neutral:')
		but_emo_shortcut_neutral = F.add(nps.ButtonPress, name='Enter your shortcut here', when_pressed_function= lambda: emo_short(but_emo_shortcut_neutral, "neutral"))

		F.add(nps.FixedText, value='Shortcut for happy:')
		but_emo_shortcut_happy = F.add(nps.ButtonPress, name='Enter your shortcut here', when_pressed_function= lambda: emo_short(but_emo_shortcut_happy, "happy"))

		F.add(nps.FixedText, value='Shortcut for angry:')
		but_emo_shortcut_sad = F.add(nps.ButtonPress, name='Enter your shortcut here', when_pressed_function= lambda: emo_short(but_emo_shortcut_sad, "angry"))
		
		F.edit()


def emo_short(button: nps.ButtonPress, emo:str):
	COMM = 'Press your shortcut'

	button.name = COMM
	shortcut = kb.record() # Deleting escape
	if shortcut and shortcut[-1].name == 'esc':
		shortcut.pop()
	if shortcut and shortcut[0].name == 'enter':
		shortcut.pop(0)
	if len(shortcut)>0:
		button.name = get_text_shortcut(shortcut)
		EMO_SHORTCUTS[emo] = shortcut


def get_text_shortcut(srtc: list[kb.KeyboardEvent]) -> str:
	return " + ".join((i.name for i in srtc if i.event_type == 'down'))


def sublist(lst1, lst2):
   ls1 = [element for element in lst1 if element in lst2]
   ls2 = [element for element in lst2 if element in lst1]
   return ls1 == ls2 and len(ls1)>=len(ls2) and len(ls2)>0


def gen_emotion(emo: str) -> tuple[bool, str]:
	"""Zwraca feedback"""
	kb.play(EMO_SHORTCUTS['neutral'])
	sleep(0.2)
	kb.play(EMO_SHORTCUTS[emo])
	notification.notify(title= "New emotion",
						message= f"Your emotion was changed to {emo}",
						timeout= 5)
	kb.start_recording()
	sleep(10)
	found = kb.stop_recording()
	print(found)
	for name, e in EMO_SHORTCUTS.items():
		if sublist(found, e):
			if name == emo:
				return False, 'neutral'
			else:
				return False, name
	return True, emo


if __name__ == "__main__":
	App = Menu()
	App.run()
	print(EMO_SHORTCUTS)
	sleep(3)
	for i in ('happy', 'angry'):
		print(gen_emotion(i))
