from validclust import ValidClust
from tqdm import tqdm
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class CoverageSpecificity():
    def __init__(self, data, cluster_k_min=2, cluster_k_max=11, cov_sp_xlim_right=None, cov_sp_xlim_left=None):
        self.cluster_k_min = cluster_k_min
        self.cluster_k_max = cluster_k_max
        self.symbols_t = ['vl','l','m','h','vh']
        self.symbols = list(range(1,7))
        self.cov_sp_xlim_right = cov_sp_xlim_right
        self.cov_sp_xlim_left = cov_sp_xlim_left
        self.data = data
        
    def specificity(self, r):
        return 1 - r

    def coverage(self, r, data, cluster_center):
        s = 0
        for row in data:
            dist = np.abs(np.array(row) - np.array(cluster_center))
            if all(dist <= cluster_center.shape[0] * r):
                s += 1
        return s / data.shape[0]

    def find_x(self, x1,x2, r):
        return r[np.argsort(np.abs(x1 - x2))[0]]
    
    def cov_sp(self, cluster_centers, cl_number):
        coverages = []
        coverages_max = []
        labels = []
        sp = []
        r = np.arange(0, 1, 0.01)
        plt.figure(figsize=(16,8))
        xs = []
        plt.title(f'coverage and specificity for #of clusters {len(cluster_centers)}')
        for i, cl_center in enumerate(cluster_centers):
            for rad in r:
                cov = self.coverage(rad, self.data, cl_center)
                coverages.append(cov)
                sp.append(self.specificity(rad))
            coverages = np.array(coverages)
            coverages_max.append(coverages)
            plt.plot(r, coverages)
            x = self.find_x(coverages, sp, r)
            xs.append(x)
            coverages = []
            sp = []
        labels.extend([f'coverage of cluster #{i}' for i in range(cl_number)])
        for rad in r:
            sp.append(self.specificity(rad))
        plt.plot(r, sp)
        labels.extend(['specificity'])
        
        
        cov_sp_return = []
        cov_sp_dot_max = [] 
        for cv_arr in coverages_max:
            cv_spec_mult = sp * cv_arr
            ind = np.argmax(cv_spec_mult)
            cov_sp_return.append(cv_spec_mult)
            cov_sp_dot_max.append((np.arange(0, 1, 0.01)[ind],cv_spec_mult[ind]) )
            plt.plot(np.arange(0, 1, 0.01), cv_spec_mult)
        labels.extend([f'cross product of coverage and specificity for cluster {i}' 
                       for i in range(len(coverages_max))])
        
        pos_prev = 1.1
        prev_x = None
        j = 0
        for x_y_pair in cov_sp_dot_max:
            x, y = x_y_pair
            if prev_x and prev_x - x <=.05:
                pass
            else:
                prev_x = x
                plt.axvline(x=x, linestyle='dashed', alpha=0.7)
                plt.annotate(f'x = {x}', (x, pos_prev))
                labels.append(f'maximum value for coverage specificity cross product for cluster {j} equal {y}')
                pos_prev -= 0.1 
            j += 1
        
        plt.legend(labels);
        plt.xlim(right=self.cov_sp_xlim_right)
        plt.xlim(left=self.cov_sp_xlim_left)
        return xs, {'cov_sp': cov_sp_return, 'cov': coverages_max, 'sp': np.tile(sp,(len(coverages_max),1))} 

    def granulas(self, centers, rs, cov_sp_dict):
        colors= list(mcolors.TABLEAU_COLORS.keys())
        i=0
        legends = []
        
        cov = cov_sp_dict['cov']
        sp = cov_sp_dict['sp']
        cov_sp = cov_sp_dict['cov_sp']
        
        
        if self.data.shape[1] == 2:
            fig, ax = plt.subplots()
            fig.set_figheight(15)
            fig.set_figwidth(15)
            plt.scatter(self.data[:,0], self.data[:,1])
            for center, r in zip(centers, rs):
                ind = np.argmax(cov_sp[i])
                max_cov = cov[i][ind]
                max_sp = sp[i][ind]
                
                circle= plt.Circle(center, r, color=colors[i], alpha=0.5 )
                ax.add_patch(circle)
                legends.append(f'radius={r}, coverage={max_cov}, specificity={max_sp},coverage_specificity_product={cov_sp[i][ind]}')
                i+=1
                ax.autoscale()
            plt.title('2d representation of the information granulas')
            plt.legend(legends);
            plt.show()
        else:
            raise Exception('Cannot illustrate dimensions > 2')
            
    
    def in_range(self, bucket, num):
        left = bucket[0]
        right = bucket[1]
        return num >= left and num <= right

    def create_ranges(self, left, right , num_of_buckets = 5):
        return np.concatenate((np.arange(left, right, (right - left) / num_of_buckets), np.array([right])), axis=0)

    def range_from_borders(self, cl_center, rs):
        l = []
        r = []
        for center, r_ in zip(self, cl_center, rs):
            l.append(center - r_/2)
            r.append(center + r_/2)
        return min(l), max(r)

    def create_middle(self, dots):
        mds = []
        for i in range(len(dots) - 1):
            mds.append((dots[i] + dots[i + 1]) / 2)
        return mds

    def top_bucket(self, buckets, data):
        top = {}
        for i in range(5):
            top[i] = 0
        b = sliding_window_view(buckets,2)
        for point in data:
            for bucket, name_bucket in zip(b, range(5)):
                if in_range(bucket, point):
                    top[name_bucket] += 1
        return top

    def char(self, centers_1_var, rs, variable, data, labels_, variable_name):
        plt.figure(figsize=(12,8))
        for y,cr in enumerate(zip(centers_1_var, rs)):
            c,r = cr
            plt.plot((c - r/2, c + r/2),(y,y), linewidth=5)
            class_data = zip(labels_, pd_data_scaled.iloc[:,variable])
            d = [elem[1] for elem in (filter(lambda x: x[0] == y, class_data))]
            l,r = self.range_from_borders(centers_1_var, rs)
            splits = self.create_ranges(l,r)
            tp_bucks = self.top_bucket(splits, d)
            label_places = self.create_middle(splits)
            for split, label_place, tp_bucks in zip(splits,label_places,tp_bucks.values()):
                plt.annotate(f' {tp_bucks}', (label_place, y))

        label_places = create_middle(splits)

        for split, label_place, label in zip(splits,label_places,symbols_t):
            plt.axvline(x=split,linestyle='dashed', alpha=0.7)
        plt.title(f'Clusters with optimal radius for variable: {variable_name}')
        plt.autoscale()
        plt.show()
        
    def draw_valid(self):
        vclust = ValidClust(
            k=list(range(self.cluster_k_min, self.cluster_k_max)), 
            methods=['kmeans']
        )
        cvi_vals = vclust.fit_predict(self.data)
        df1 = cvi_vals.reset_index()
        labels = []
        cal_scaler =  MinMaxScaler()

        indices_data = []
        for idx, row in df1.iterrows():
            l = row.values[1]
            if l == 'calinski':
                labels.append('calinski scaled from 0 to 1')
                r = np.squeeze(cal_scaler.fit_transform(row.values[2:].reshape(-1, 1)))
            else:
                if l == 'davies':
                    labels.append(l + ' inverse')
                    r = -row.values[2:]
                else:
                    labels.append(l)
                    r = row.values[2:]
            indices_data.append(r)

        plt.figure(figsize=(16,8))
        for row in  indices_data:
            plt.plot(range(2,11), row)

        dotes = []
        for line in indices_data:
            i = np.argsort(-line)
            dotes.append((i[0] + 2, line[i[0]]))

        dotes2 = np.array(dotes)
        for dot in dotes2:
            x1,y1 = dot
            plt.axvline(x=x1,linestyle='dashed', alpha=0.7)
            plt.annotate(f'x = {x1}', (x1, y1))
        plt.legend(labels);
        plt.show()
        return {elem[0]: elem[1] for elem in zip(labels, dotes2)}
