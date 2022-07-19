from pyNN.nest import *
import math
parameters = {  'tau_m'      : 24.0,# (ms)
              'tau_syn_E'  : 2.0,# (ms)  #3
              'tau_syn_I'  : 4.0,# (ms)  #9
              'i_offset'   : 0.0,
              'tau_refrac' : 3.0,# (ms)
              'v_rest'     : -65.0,# (mV)
              'v_reset'    : -65.0,# (mV)
              'v_thresh'   : -45.0,# (mV)
              'cm'         : 1.0
}

class Layer:
    def __init__(self,name):
        self.name = name
        #self.weights = = []
        self.populations = []
        self.population_sizes = []
        
    def add_populations(self,neurons_type,neurons_array, spike_input = None):
        for population_id in range(len(neurons_array)):
            self.population_sizes.append(neurons_array[population_id])
            if spike_input != None:
                self.populations.append(Population(neurons_array[population_id],neurons_type,{'spike_times': spike_input},label=self.name))
            else:
                global parameters
                self.populations.append(Population(neurons_array[population_id],neurons_type,parameters,label=str(population_id) + "_" + self.name))
    
    def connect_layers(self,other_layer,connection_type,weights,stdp = None):
        projections = []
        if connection_type == "all":
            for population in self.populations:
                for other_population in other_layer.populations:
                    if stdp != None:
                        projections.append(Projection(population, other_population, AllToAllConnector(allow_self_connections=False),stdp,StaticSynapse(weight=weights), label=self.name + "_" + other_layer.name))
                    else:
                        projections.append(Projection(population, other_population, AllToAllConnector(allow_self_connections=False),StaticSynapse(weight=weights), label=self.name + "_" + other_layer.name))
        else:
            for i in range(len(self.populations)):
                if connection_type == "one":
                    if stdp == None:
                        projections.append(Projection(self.populations[i], other_layer.populations[i], OneToOneConnector(),StaticSynapse(weight=weights), label=self.name + "_" + other_layer.name))
                    else:
                        projections.append(Projection(self.populations[i], other_layer.populations[i], OneToOneConnector(), stdp,StaticSynapse(weight=weights), label=self.name + "_" + other_layer.name))
                else:
                    if stdp == None:
                        projections.append(Projection(self.populations[i], other_layer.populations[0], OneToOneConnector(),StaticSynapse(weight=weights), label=self.name + "_" + other_layer.name))
                    else:
                        projections.append(Projection(self.populations[i], other_layer.populations[0], OneToOneConnector(), stdp,StaticSynapse(weight=weights), label=self.name + "_" + other_layer.name))
        return projections
    
    def connect_with_given_kernel_weights(self,other_layer,kernel_weights): 
        projections = []
        first_population_dimension = int(math.sqrt(self.population_sizes[0]))
        for population_id in range(len(other_layer.populations)):    
            connection_list = []
            second_population_dimension = int(math.sqrt(other_layer.population_sizes[population_id]))
            for x in range(second_population_dimension):
                for y in range(second_population_dimension):
                    for kernel_x in range(kernel_weights[population_id].shape[0]):
                        for kernel_y in range(kernel_weights[population_id].shape[1]):
                            connection_list.append((x + kernel_x + (y + kernel_y) * first_population_dimension,x + y * second_population_dimension,kernel_weights[population_id][kernel_x][kernel_y],1.0))
                            
            projections.append(Projection(self.populations[0], other_layer.populations[population_id], FromListConnector(connection_list), label=self.name + "_" + other_layer.name))
         
        return projections        
    
    def connect_with_subsampling(self,other_layer,weight,stdp):
        projections = []
        first_population_dimension = int(math.sqrt(self.population_sizes[0]))
        for population_id in range(len(other_layer.populations)):
            connection_list = []
            for x in range(first_population_dimension):
                for y in range(first_population_dimension):
                    connection_list.append((x * first_population_dimension + y,(first_population_dimension // 2) * (x // 2) + (y // 2),weight,1.0))
                    
            projections.append(Projection(self.populations[population_id], other_layer.populations[population_id], FromListConnector(connection_list),stdp,label=self.name + "_" + other_layer.name))
            
        return projections
    
    def winner_takes_all(self,weight):
        connections = []
        for index in range(self.population_sizes[0]):
            for index2 in range(self.population_sizes[0]):
                if index != index2:
                    connections.append((index,index2,weight * 1.2,1.0))
                else:
                    connections.append((index,index2,weight,1.0))
        return Projection(self.populations[0],self.populations[0],FromListConnector(connections))