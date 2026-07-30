def center(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2) // 2, (y1 + y2) // 2)


def inside(small_box, big_box):

    cx, cy = center(small_box)

    x1, y1, x2, y2 = big_box

    return x1 <= cx <= x2 and y1 <= cy <= y2


def overlap(box1, box2):

    x1, y1, x2, y2 = box1
    a1, b1, a2, b2 = box2

    ix1 = max(x1, a1)
    iy1 = max(y1, b1)

    ix2 = min(x2, a2)
    iy2 = min(y2, b2)

    return max(0, ix2 - ix1) * max(0, iy2 - iy1)


def find_violators(riders, no_helmets):

    violators = []

    for rider in riders:

        for nh in no_helmets:

            if inside(nh, rider):
                violators.append(rider)
                break

    return violators


def find_vehicle(rider, vehicles):

    best = None
    best_overlap = 0

    for vehicle in vehicles:

        ov = overlap(rider, vehicle)

        if ov > best_overlap:
            best_overlap = ov
            best = vehicle

    return best


def find_plate(vehicle, plates):

    if vehicle is None:
        return None

    for plate in plates:

        if inside(plate, vehicle):
            return plate

    return None