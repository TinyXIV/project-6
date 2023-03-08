"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""

import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
BREVET_SPEEDS = {
    200: [(15, 34), (15, 32)],
    300: [(15, 32), (15,32)],
    400: [(15, 32), (15, 30)],
    600: [(15, 30), (11.428, 28)],
    1000: [(11.428, 28), (13.333, 26)]
}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
       
       brevet_dist_km: always starts at start time and closes after an hour
                            (already known)
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    if control_dist_km <= 0:
       return brevet_start_time


    total_time = 0
    last_checkpoint_dist = 0



    if control_dist_km >= brevet_dist_km:
       # Control distance is greater than or equal to the brevet distance
       for distance, speeds in BREVET_SPEEDS.items():
           if distance >= brevet_dist_km:
              speed = BREVET_SPEEDS[distance][0][1] #  # Maximum speed for the appropriate control location range
              total_time += (control_dist_km - last_checkpoint_dist) / speed * 60
              break
           else:
              speed = BREVET_SPEEDS[distance][0][1]
              total_time += (distance - last_checkpoint_dist) / speed * 60
              last_checkpoint_dist = distance
              
       hours, minutes = divmod(total_time, 60)
       minutes = round(minutes, 0)
       return brevet_start_time.shift(hours= hours, minutes= minutes)

    
    for distance, speeds in BREVET_SPEEDS.items():
       if control_dist_km <= distance:
           speed = BREVET_SPEEDS[distance][0][1] #  # Maximum speed for the appropriate control location range
           total_time += (control_dist_km - last_checkpoint_dist) / speed * 60
           break
       else:
           speed = BREVET_SPEEDS[distance][0][1]# max speed for distance
           total_time += (distance - last_checkpoint_dist) / speed * 60
           last_checkpoint_dist = distance

    hours, minutes = divmod(total_time, 60)
    minutes = round(minutes, 0)
    return brevet_start_time.shift(hours = hours, minutes=minutes)

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
       
       brevet_dist_km: need to figure where 1st and last checkpoint is/are
              by if your control dist is greater or equal to your brevet dist
              then it is your last checkpoint.
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    if control_dist_km <= 0:
       #Increment an hour from the start time
       return brevet_start_time.shift(hours = 1)
       
    
       
    if control_dist_km >= brevet_dist_km:
       if control_dist_km == 200:
           #According to https://rusa.org/pages/acp-brevet-control-times-calculator
           '''
           By the rules, the overall time limit for a 200km brevet is 13H30, even though by calculation, 
           200/15 = 13H20. The fact that the route is somewhat longer than 200km is irrelevant.
           '''
           return brevet_start_time.shift(hours= 13, minutes= 30)
       elif control_dist_km > 600:
           distance = control_dist_km - 600
           total_time = 600/15 * 60
           total_time += distance / 11.428 * 60
           hours, minutes = divmod(total_time, 60)
           minutes = round(minutes, 0)
           return brevet_start_time.shift(hours= hours, minutes= minutes)
       else:
           # Control distance is greater than or equal to the brevet distance
           speed = BREVET_SPEEDS[brevet_dist_km][0][0]
           total_time = brevet_dist_km / speed * 60
           hours, minutes = divmod(total_time, 60)
           minutes = round(minutes, 0)
           return brevet_start_time.shift(hours= hours, minutes= minutes)

       

    if control_dist_km < 60:
       #French variation that became allowed outside of france in 2018,
       #which uses 20km/hr to prevent errors within the first 60km
       #that occurs when using the standard algorithm

       total_time = (control_dist_km / 20) * 60
       hours, minutes = divmod(total_time, 60)
       minutes = round(minutes, 0)
       hours = (hours +1)
       return brevet_start_time.shift(hours= hours, minutes= minutes)
       

    total_time = 0
    last_checkpoint_dist = 0
    
    

    
    for distance in sorted(BREVET_SPEEDS.keys()):
       if control_dist_km <= distance:
           speed = BREVET_SPEEDS[distance][0][0]
           total_time += (control_dist_km - last_checkpoint_dist) / speed * 60
           break
       else:
           # Control is at or before last checkpoint
           speed = BREVET_SPEEDS[distance][0][0]
           total_time += (distance - last_checkpoint_dist) / speed * 60
           last_checkpoint_dist = distance
       

    hours, minutes = divmod(total_time, 60)
    minutes = round(minutes, 0)
    return brevet_start_time.shift(hours = hours, minutes=minutes)

