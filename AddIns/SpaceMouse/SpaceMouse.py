#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import threading, random, json, socket, array, math

HOST = "127.0.0.1"
PORT = 11111

app = None
ui = None
handlers = []
stopFlag = None
myCustomEvent = 'MyCustomEventId'
customEvent = None

mysock = None

check = False

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

# The event handler that responds to the custom event being fired.
class ThreadEventHandler(adsk.core.CustomEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            global app

            rotx_en = roty_en = rotz_en = movx_en = movy_en = movz_en = False

            rotx_en = True
            roty_en = True
            rotz_en = True
            movx_en = True
            movy_en = True
            movz_en = True

            eventArgs = json.loads(args.additionalInfo)

            rx = eventArgs['rx']
            ry = eventArgs['ry']
            rz = eventArgs['rz']
            x = eventArgs['x']
            y = eventArgs['y']
            z = eventArgs['z']

            # get state
            vi = app.activeViewport
            camera = vi.camera #This is a deep copy.
            eye = camera.eye
            tgt = camera.target
            up = camera.upVector

            # calc coef
            coef = math.sqrt(camera.viewExtents)

            MOV_COEF = 0.0002 * coef
            ROT_COEF = 0.00015
            TILT_COEF = 0.00007
            ZOOM_COEF = 0.0005 * coef


            # get matrix
            front = eye.vectorTo(tgt)
            right = front.crossProduct(up)

            matr = adsk.core.Matrix3D.create()
            matr.setWithCoordinateSystem(eye, right, front, up)

            if rotx_en:
                rotx = adsk.core.Matrix3D.create()
                rotx.setToRotation(-rx * TILT_COEF, right, tgt)

                matr.transformBy(rotx)

            if rotz_en:
                rotz = adsk.core.Matrix3D.create()
                rotz.setToRotation(-ry * ROT_COEF, up, tgt)

                matr.transformBy(rotz)

            if roty_en:
                roty = adsk.core.Matrix3D.create()
                roty.setToRotation(-rz * TILT_COEF, front, tgt)

                matr.transformBy(roty)

            (eye, right, front, up) = matr.getAsCoordinateSystem()

            if movx_en:
                movx = right.copy()
                movx.normalize()
                movx.scaleBy(-x * MOV_COEF)

                eye.translateBy(movx)
                tgt.translateBy(movx)

            if movy_en:
                movy = up.copy()
                movy.normalize()
                movy.scaleBy(-y * MOV_COEF)

                eye.translateBy(movy)
                tgt.translateBy(movy)

            if movz_en:
                ve = camera.viewExtents
                ve += z * ZOOM_COEF
                if ve > 0:
                    camera.viewExtents = ve


            # write back
            camera.isSmoothTransition = False

            camera.target = tgt
            camera.eye = eye
            camera.upVector = up
            vi.camera = camera
            vi.refresh()

            #adsk.doEvents()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# The class for the new thread.
class MyThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        global mysock

        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysock.connect((HOST, PORT))

        while True:
            data = mysock.recv(32)
            arr = array.array('i', data)
            if arr[0] == 0:
                args = {'x': arr[1], 'y': arr[2], 'z': arr[3], 'rx': arr[4], 'ry': arr[5], 'rz': arr[6]}
                app.fireCustomEvent(myCustomEvent, json.dumps(args))

def run(context):
    global ui
    global app

    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        ui.messageBox('SpaceMouse start !!!')

        # Register the custom event and connect the handler.
        global customEvent
        customEvent = app.registerCustomEvent(myCustomEvent)

        onThreadEvent = ThreadEventHandler()
        customEvent.add(onThreadEvent)
        handlers.append(onThreadEvent)

        # Create a new thread for the other processing.
        global stopFlag
        stopFlag = threading.Event()
        myThread = MyThread(stopFlag)
        myThread.start()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    global mysock
    try:
        mysock.close()

        if handlers.count:
            customEvent.remove(handlers[0])

        stopFlag.set()
        app.unregisterCustomEvent(myCustomEvent)
        ui.messageBox('Stop addin')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
