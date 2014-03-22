drivers = []
remove_next_tick = []

def update(dT):
    for driver in remove_next_tick:
        driver.done = True
        drivers.remove(driver)
    while len(remove_next_tick) > 0:
        remove_next_tick.pop()

    for driver in drivers:
        if driver.update(dT):
            remove_next_tick.append(driver)

    

def addDriver(driver):
    drivers.append(driver)
    driver.remove_next_tick = False
