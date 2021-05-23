from re import sub
import keyboard as kb
import npyscreen as nps
from time import sleep
from plyer import notification

WORDARD = """
                            .
                            |
;-.-. ,-. ,-. ,-. ,-. ,-. ,-|
| | | | | | | | | | | | | | |
' ' ' `-' `-' `-' `-' `-' `-'
"""

INFO = """
moooood is an EEG-based emotion tracker used for virtual avatars.
To set up your avatar, provide us with the keyboard shortcuts you use 
to activate emotions in your avatar and start tracking.
To provide a shortcut: 1) select a field, 2) Press enter, 
3) Press the desired shortcut, 4) Press escape.
"""

class NoBullShitText(nps.Pager):
    def __init__(self, *args, **kwargs):
        kwargs["height"] = kwargs["text"].count("\n")+1
        kwargs["values"] = kwargs["text"].split("\n")
        kwargs["autowrap"] = True
        kwargs["editable"] = False
        del(kwargs["text"])
        
        nps.Pager.__init__(self, *args, **kwargs)

class Menu(nps.NPSApp):


    def __init__(self) -> None:
        super().__init__()
        self.EMO_SHORTCUTS = {}


    def main(self):
        F  = nps.Form()

        F.add(NoBullShitText, text=WORDARD)

        F.add(NoBullShitText, text=INFO)

        F.add(nps.FixedText, value='Add a keyboard shortcut for the neutral expression:', editable=False)
        but_emo_shortcut_neutral = F.add(nps.ButtonPress, name='Enter your shortcut here', when_pressed_function= lambda: self.emo_short(but_emo_shortcut_neutral, "neutral"))

        F.add(nps.FixedText, value='Add a keyboard shortcut for the happy expression:', editable=False)
        but_emo_shortcut_happy = F.add(nps.ButtonPress, name='Enter your shortcut here', when_pressed_function= lambda: self.emo_short(but_emo_shortcut_happy, "happiness"))

        F.add(nps.FixedText, value='Add a keyboard shortcut for the sad expression:', editable=False)
        but_emo_shortcut_sad = F.add(nps.ButtonPress, name='Enter your shortcut here', when_pressed_function= lambda: self.emo_short(but_emo_shortcut_sad, "sadness"))
        
        F.edit()


    def emo_short(self, button: nps.ButtonPress, emo: str):
        shortcut = kb.record()
        if shortcut and shortcut[-1].name == 'esc': # Deleting escapes
            shortcut.pop()
        if shortcut and shortcut[0].name == 'enter': # Deleting enters
            shortcut.pop(0)
        if len(shortcut)>0:
            button.name = get_text_shortcut(shortcut)
            self.EMO_SHORTCUTS[emo] = shortcut


    def gen_emotion(self, emo: str) -> tuple[bool, str]:
        """Zwraca feedback"""
        val = self.EMO_SHORTCUTS.get(emo, None)
        if val is None:
            return None
            
        kb.play(self.EMO_SHORTCUTS['neutral'])
        sleep(0.4)
        kb.play(val)
        notification.notify(title= "New emotion",
                            message= f"Your emotion was changed to {emo}",
                            timeout= 1)
        kb.start_recording()
        sleep(10)
        found = kb.stop_recording()
        for name, e in self.EMO_SHORTCUTS.items():
            if sublist(found, e):
                if name == emo:
                    return False, 'neutral'
                else:
                    return False, name
        return True, emo


def get_text_shortcut(srtc: list[kb.KeyboardEvent]) -> str:
    return " + ".join((i.name for i in srtc if i.event_type == 'down'))


def sublist(lst1, lst2):
   ls1 = [element for element in lst1 if element in lst2]
   ls2 = [element for element in lst2 if element in lst1]
   return ls1 == ls2 and len(ls1)>=len(ls2) and len(ls2)>0