class ApplianceGroup(object):
    """
    Implements many of the same methods as Appliance.
    
    Attributes
    ----------
    items : dict of Appliance or ApplianceGroup objects 
    """
    def __getattr__(self, key):
        """Gets a single appliance.
        If no instance is specified then default to 1.
        e.g. appliancegroup['toaster'] or ['toaster', 2]
        """
        raise NotImplementedError
            
    def select(self, *args, **kwargs):
        """
        e.g. 
        * select(category='lighting')
        * select(category=['ict', 'lighting'])
        * select([(fridge, 1), (tv, 1)]) # get specifically fridge 1 and tv 1
        * select(name=['fridge', 'tv']) # get all fridges and tvs
        * select(category='lighting', except={'room'=['kitchen lights']})
        * select('all', except=[('tv', 1)])
        
        TODO: see if we can do select(category='lighting' | name='tree lights')
        or select(energy > 100)??  Perhaps using:
        * Python's eval function something like this:
          >>> s = pd.Series(np.random.randn(5))
          >>> eval('(x > 0) | (index > 2)', {'x':s, 'index':s.index})
          Hmm, yes, maybe we should just implement this!  e.g.
          select("(category == 'lighting') | (category == 'ict')")
          
          But what about:
          * select('total_energy > 100')
          * select('mean(hours_on_per_day) > 3')
          * select('max(hours_on_per_day) > 5')
          * select('max(power) > 2000')
          * select('energy_per_day > 2')
          * select('rank_by_energy > 5') # top_k(5)
          * select('rank_by_proportion > 0.2')
          Maybe don't bother.  That's easy enough
          to get with itemised_energy().  Although these are quite nice
          and shouldn't be too hard.  Would need to only calculate
          these stats if necessary though (e.g. by checking if 'total_energy'
          is in the query string before running `eval`)
          
        * or numexpr: https://github.com/pydata/numexpr
        * see Pandas.eval(): 
          * http://pandas.pydata.org/pandas-docs/stable/indexing.html#the-query-method-experimental
          * https://github.com/pydata/pandas/blob/master/pandas/computation/eval.py#L119
        
        Returns
        -------
        A new ApplianceGroup
        """
        raise NotImplementedError
        
    def groupby(self, **kwargs):
        """
        e.g. groupby('category')
        
        Returns
        -------
        A new ApplianceGroup or ApplianceGroup objects
        """
        raise NotImplementedError
        
    def total_on_duration(self):
        """Return timedelta"""
        raise NotImplementedError
    
    def on_durations(self):
        self.get_unique_upstream_meters()
        # for each meter, get the on time, 
        # assuming the on-power-threshold for the 
        # smallest appliance connected to that meter???
        raise NotImplementedError
    
    def activity_distribution(self, bin_size, timespan):
        raise NotImplementedError
    
    def when_on(self, on_power_threshold):
        """Return Series of bools"""
        raise NotImplementedError
    
    def cross_correlation(self):
        """Correlation between items."""
        raise NotImplementedError
        
    def all_unique_meters(self):
        """Returns a set of all unique meters.  
        Some meters might measure the same appliances."""
        raise NotImplementedError
        
    def unique_meters_without_double_counting(self):
        """Returns a set of all meters ensuring that each appliance only appears once."""
        # Gets unique meters from all appliances in this ApplianceGroup
        # Creates graph of meters.  
        # Removes all but the furthest upstream meters.
        # Warns if we also measure energy for one or more appliances not in selection
        raise NotImplementedError
        
    def total_energy(self):
        self.get_unique_upstream_meters()
        # adds energy on a meter-by-meter basis
        raise NotImplementedError
    
    def on_off_events(self, minimum_state_duration):
        raise NotImplementedError
    
    def top_k(self, k=5):
        """Return new ApplianceGroup?"""
        self.itemised_energy().ix[:k]
    
    def itemised_energy(self):
        """ Needs to do it per-meter???  Return sorted.
        'kitchen lights': 234.5
        ['hall lights, bedroom lights'] : 32.1 
        need to subtract kitchen lights energy from lighting circuit!
        """ 
        # keys could be actual Appliance / ApplianceGroup objects?
        # e.g. when we want to select top_k Appliances.
        raise NotImplementedError
        
    def proportion_above(self, threshold_proportion):
        """Return new ApplianceGroup with all appliances whose proportion of
        energy usage is above threshold"""
        raise NotImplementedError
        
    def itemised_proportions(self):
        """Proportion of energy per appliance. Return sorted."""
        raise NotImplementedError
    
    def power_series(self):
        # Get all upstream meters. Add series.  Return generator of series.
        # What happens if indicies don't match?  Automatically re-sample?  Or down-sample?
        # Probably best to raise exception and make user pre-process???  How?
        # lighting.resample('6S').power_series() ???? or
        # lighting.preprocessing = [Resample('6S')]
        # lighting.power_series()
        raise NotImplementedError
            
    def init_new_dataset(self):
        self.infer_and_set_meter_connections()
        self.infer_and_set_dual_supply_appliances()
            
    def infer_and_set_meter_connections(self):
        """
        Arguments
        ---------
        meters : list of Meter objects
        """
        # Maybe this should be a stand-alone function which
        # takes a list of meters???
        raise NotImplementedError
        
    def infer_and_set_dual_supply_appliances(self):
        raise NotImplementedError
    
    def plot(self, how='stacked'):
        """
        Arguments
        ---------
        stacked : {'stacked', 'heatmap', 'lines', 'snakey'}
        """
        # pretty snakey:
        # http://www.cl.cam.ac.uk/research/srg/netos/c-aware/joule/V4.00/
        raise NotImplementedError
