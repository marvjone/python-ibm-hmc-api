from hmcapi.hmcapi import HMCAPI

def activate_processors():
    '''
    This function will activate processors on a ibm hmc server over ssh
    '''
    hmc = hmcapi.HMCAPI(hostname='10.0.2.34',
                        username='hmcuser',
                        password='hmcpassword')

        result = hmc.capacity_on_demand(managed_system_name='ibmpowerserver01',
                                        capacity_on_demand_code='23321321332132132132132131321')
    return result