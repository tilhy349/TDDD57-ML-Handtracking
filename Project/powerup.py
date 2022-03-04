from settings import *

class PowerupHandler:

    def __init__(self):
        #Power up variables
        self.available_powerups = MAX_POWERUPS
        self.current_powerup = Powerup.DEFAULT
        self.time_powerup_current = 0
        self.player_color = (255, 0, 0)
        
        self.interval = POWERUP_ENDING_LIMIT
    
    def set(self, current_gesture):
        #If no power up is currently running and we can afford to do a power up 
        if self.current_powerup == Powerup.DEFAULT and self.available_powerups > 0:
            #Check and process current gesture
            if current_gesture == Gesture.PEACE:
                self.current_powerup = Powerup.SLOWMOTION
                self.available_powerups -= 1
                self.player_color = COLOR_PEACE

            elif current_gesture == Gesture.CLOSE:
                self.current_powerup = Powerup.INVISIBLE
                self.available_powerups -= 1
                self.player_color = COLOR_CLOSE

    def process(self, dt, n_coins):       
        
        #If a power is used -> start counting the time
        if self.current_powerup != Powerup.DEFAULT:
            self.time_powerup_current += dt / 60
            
            if self.time_powerup_current > self.interval : #two seconds left of power-up, blink every 1/4 seconds 
                self.interval += POWERUP_BLINK_STEP 
                
                if self.player_color != COLOR_ORIGINAL :
                    self.player_color = COLOR_ORIGINAL
                else: 
                    if self.current_powerup == Powerup.SLOWMOTION:
                        self.player_color = COLOR_PEACE
                    else:
                        self.player_color = COLOR_CLOSE
            
            #If the timer reaches the limit, reset timer and current power-up
            if self.time_powerup_current > POWERUP_TIME_LIMIT:
                self.current_powerup = Powerup.DEFAULT
                self.time_powerup_current = 0
                self.player_color = COLOR_ORIGINAL
                self.interval = POWERUP_ENDING_LIMIT     
        
        #If available power-ups is not max and we can afford a new power-up, buy new power-up
        if self.available_powerups < MAX_POWERUPS and n_coins >= POWERUP_COST:
            self.available_powerups += 1
            n_coins -= POWERUP_COST
        
        return n_coins