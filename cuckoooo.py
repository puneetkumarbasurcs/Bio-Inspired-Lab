import numpy as np
import scipy.special as special

np.random.seed(42)

def medical_threshold_objective(thresholds):
    target = np.array([148.0, 52.0]) 
    return np.sum((thresholds - target) ** 2)

class CuckooSearchEngine:
    def __init__(self, objective_func, space_bounds):
        self.obj_func = objective_func
        self.bounds = np.array(space_bounds)
        self.dim = len(space_bounds)
        
    def _levy_flight(self, beta=1.5):
        num = special.gamma(1 + beta) * np.sin(np.pi * beta / 2)
        den = special.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)
        sigma_u = (num / den)**(1 / beta)
        
        u = np.random.normal(0, sigma_u, self.dim)
        v = np.random.normal(0, 1, self.dim)
        return u / (np.abs(v)**(1 / beta))

    def execute_search(self, num_nests=20, pa=0.25, max_iterations=100):
       
        nests = np.random.uniform(self.bounds[:, 0], self.bounds[:, 1], (num_nests, self.dim))
        
        fitness = np.apply_along_axis(self.obj_func, 1, nests)
        
        best_idx = np.argmin(fitness)
        best_nest = nests[best_idx].copy()
        best_fitness = fitness[best_idx]

        for iteration in range(max_iterations):
            if (iteration + 1) % 25 == 0 or iteration == 0:
                print(f" Iteration {iteration + 1:03d} | Current Best Thresholds: {np.round(best_nest)} | Error: {best_fitness:.4f}")
            
          
            for i in range(num_nests):
                step = self._levy_flight()
                step_size = 0.01 * step * (nests[i] - best_nest)
                
                new_nest = np.clip(nests[i] + step_size, self.bounds[:, 0], self.bounds[:, 1])
                new_fitness = self.obj_func(new_nest)
                
                j = np.random.randint(0, num_nests)
                if new_fitness < fitness[j]:
                    nests[j] = new_nest
                    fitness[j] = new_fitness

           
            for i in range(num_nests):
                if np.random.rand() < pa:
                    r1, r2 = np.random.randint(0, num_nests, 2)
                    step_size = np.random.rand() * (nests[r1] - nests[r2])
                    
                    nests[i] = np.clip(nests[i] + step_size, self.bounds[:, 0], self.bounds[:, 1])
                    fitness[i] = self.obj_func(nests[i])

            current_best = np.argmin(fitness)
            if fitness[current_best] < best_fitness:
                best_fitness = fitness[current_best]
                best_nest = nests[current_best].copy()

       
        return best_nest, best_fitness

if __name__ == "__main__":
    pixel_bounds = [(0, 255), (0, 255)]
    
    print(" Initializing Cuckoo Search Engine Optimization Loop...\n")
    cs_engine = CuckooSearchEngine(medical_threshold_objective, space_bounds=pixel_bounds)
    optimal_thresholds, final_error = cs_engine.execute_search(num_nests=15, pa=0.20, max_iterations=100)
    
    print("\n Optimization Completed Successfully!")
    print(f"Optimal Image Grayscale Thresholds Found : {np.round(optimal_thresholds)}")
    print(f"Final Optimization Error Metric          : {final_error:.6f}")
