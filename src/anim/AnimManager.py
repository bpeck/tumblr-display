drivers = []
remove_next_tick = []

def update(dT):
    global remove_next_tick, drivers
    for driver in remove_next_tick:
        driver.done = True
        drivers.remove(driver)
        driver.onRemove()

    remove_next_tick = []

    for driver in drivers:
        if driver.update(dT):
            remove_next_tick.append(driver)


def addDriver(driver):
    drivers.append(driver)
