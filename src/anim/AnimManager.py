drivers = []

def update(dT):
    remove = []

    for driver in drivers:
        if driver.update(dT):
            remove.append(driver)

    for driver in remove:
        drivers.remove(driver)

def addDriver(driver):
    drivers.append(driver)
