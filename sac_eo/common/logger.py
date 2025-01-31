import numpy as np
import pickle
import os

class Logger:
    """Class for logging data throughout training."""

    def __init__(self):
        self.param_dict = dict() # Parameter inputs
        self.train_dict = dict() # Training data
        self.final_dict = dict() # Final NN weights and normalization stats
    
    def log_train(self,kv):
        for k,v in kv.items():
            if k in self.train_dict.keys():
                self.train_dict[k].append(v)
            else:
                self.train_dict[k] = [v]
    
    def log_train_ensemble(self,kv_list):
        ensemble_dict = dict()
        for kv in kv_list:
            for k,v in kv.items():
                if k in ensemble_dict.keys():
                    ensemble_dict[k].append(v)
                else:
                    ensemble_dict[k] = [v]
        
        ensemble_dict_np = dict()
        for k,v in ensemble_dict.items():
            ensemble_dict_np[k] = np.array(v)
        
        self.log_train(ensemble_dict_np)
    
    def log_params(self,kv):
        for k,v in kv.items():
            self.param_dict[k] = v

    def log_final(self,kv):
        for k,v in kv.items():
            self.final_dict[k] = v

    def dump(self):
        """Returns dictionary of logged data."""
        train_out = dict()
        for k,v in self.train_dict.items():
            train_out[k] = np.array(v)
        
        out = {
            'param': self.param_dict,
            'train': train_out,
            'final': self.final_dict
        }

        return out

    def dump_and_save(self,log_path,log_name):
        """Saves dictionary of logged data.

        Attempts to append logged data to existing saved data if file name
        already exists, otherwise saves logged data to new file.
        
        Args:
            log_path (str): path where logged data should be saved
            log_name (str): name of file for saving logged data
        """
        out = self.dump()
        os.makedirs(log_path,exist_ok=True)
        filename = os.path.join(log_path,log_name)
        
        try:
            with open(filename,'rb') as f:
                import_data = pickle.load(f)

            for k in import_data['train'].keys():
                old = import_data['train'][k]
                if k in out['train'].keys():
                    new = out['train'][k]
                    out['train'][k] = np.concatenate((old,new),axis=0)
                else:
                    out['train'][k] = old
        except:
            pass

        with open(filename,'wb') as f:
            pickle.dump(out,f)

    def reset(self):
        self.param_dict.clear()
        self.train_dict.clear()
        self.final_dict.clear()