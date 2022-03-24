#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import threading, random, json, socket, array, math

HOST = "127.0.0.1"
PORT = 11111

app = None
ui = None
#adsk.core.UserInterface.cast(None)
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
            global last_right
            MOV_COEF = 0.001
            ROT_COEF = 0.00015
            #ROT_COEF = 0.000001
            TILT_COEF= 0.00007
            ZOOM_COEF = 0.005

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
            #rx = 100 * sign(ry)
            #ry = 100 * sign(eventArgs['ry'])

            # get state
            vi = app.activeViewport
            camera = vi.camera #This is a deep copy.
            eye = camera.eye
            tgt = camera.target
            up = camera.upVector

            #av = adsk.core.Point2D.create(0, 0)
            #bv = adsk.core.Point2D.create(vi.width, 0)
            #aw = vi.viewToModelSpace(av)
            #bw = vi.viewToModelSpace(bv)

            #scale_coef = aw.distanceTo(bw) / vi.width
            #zoom_coef = math.exp(tgt.distanceTo(eye)/100) + 1
            scale_coef = 1
            zoom_coef = 1


            #ui.messageBox('aw: ' + str(aw.asArray()) + '\nbw: ' + str(bw.asArray()))

            # get matrix
            front = eye.vectorTo(tgt)
            right = front.crossProduct(up)

            #ui.messageBox('last: ' + str(last_right.asArray()) + '\nnow: ' + str(front.asArray()) + '\nangle'+ str(front.angleTo(last_right)) + '\nright: ' + str(right.asArray()))
            #ui.messageBox('right: ' + str(right.asArray()) + '\nup: ' + str(up.asArray()) + '\neye: ' + str(eye.asArray()) + '\ntgt: ' + str(tgt.asArray()))

            check = True

            if rotx_en:
                rotx = adsk.core.Matrix3D.create()
                rotx.setToRotation(-rx * TILT_COEF, right, tgt)
                eye.transformBy(rotx)

                front_new = eye.vectorTo(tgt)
                right_new = front_new.crossProduct(up)

                #more than 180 rotation - need to change up vector direction
                if ((not right.x) or (sign(right.x) != sign(right_new.x))):
                    if ((not right.y) or (sign(right.y) != sign(right_new.y))):
                        if ((not right.z) or (sign(right.z) != sign(right_new.z))):

                            #new vectors
                            up.setWithArray([-up.x, -up.y, -up.z])
                            front.setWithArray([front_new.x, front_new.y, front_new.z])
                            right = front.crossProduct(up)

                            rotx.setToRotation(-rx * TILT_COEF, right, tgt)

                            eye = camera.eye
                            eye.transformBy(rotx)

            if rotz_en:
                eye_before = eye.copy()
                rotz = adsk.core.Matrix3D.create()
                rotz.setToRotation(-ry * ROT_COEF, up, tgt)
                eye.transformBy(rotz)

                front_new = eye.vectorTo(tgt)
                right_new = front_new.crossProduct(up)

            if roty_en:
                roty = adsk.core.Matrix3D.create()
                roty.setToRotation(-eventArgs['rz'] * TILT_COEF, front, tgt)
                up.transformBy(roty)

            if movx_en:
                movx = right.copy()
                movx.normalize()
                movx.scaleBy(-eventArgs['x'] * MOV_COEF * scale_coef)

                eye.translateBy(movx)
                tgt.translateBy(movx)

            if movy_en:
                movy = up.copy()
                movy.normalize()
                movy.scaleBy(-eventArgs['y'] * MOV_COEF * scale_coef)

                eye.translateBy(movy)
                tgt.translateBy(movy)

            if movz_en:
                ve = camera.viewExtents
                ve += eventArgs['z'] * ZOOM_COEF * zoom_coef
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
