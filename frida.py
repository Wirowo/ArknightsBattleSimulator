import frida
import sys

def on_message(message, data):
    print("[%s] => %s" % (message, data))

def main():
    device = frida.get_usb_device(timeout=1)
    session = device.attach("Arknights", realm='emulated')
    script = session.create_script("""
    var proc = Module.findBaseAddress("libil2cpp.so")
    console.log("Initiating!")

    Interceptor.attach(proc.add(0xC47750), {
        onEnter: function (args) {
            console.log("Enter Crisis Battle!")
        },
        onLeave: function (retval) {
            retval.replace(0x1)
        }
    })

""")
    script.on('message', on_message)
    script.load()
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()

if __name__ == '__main__':
    main()