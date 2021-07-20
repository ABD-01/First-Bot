import pexpect

class ChatHandler:
    def __init__(self):
        self.child = pexpect.spawn('!python interactive.py -t blended_skill_talk -mf zoo:blender/blender_1Bdistill/model', timeout=None)
        self.child.expect('Enter Your Message:')
        self.personality = self.child.before.decode('utf-8', 'ignore').split('[context]')[1]
    def listen(self):
        response = self.child.before
        resp = response.split(b'1m')
        respfinal = resp[1].split(b'\x1b')
        return respfinal[0].decode('utf-8')
    def say(self, message):
        self.child.sendline(message)
        self.child.expect('Enter Your Message:')