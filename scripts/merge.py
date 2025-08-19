import pandas as pd


speedup_df = pd.read_csv('speedup.csv')
estimate_df = pd.read_csv('estimate_only.csv')


merged_df = pd.merge(estimate_df, speedup_df, on='case', how='left')

def compute(row):
    if pd.isna(row['speedup']):
        return '-'
    else:
        return row['estimate'] - row['speedup'] + 1

result = []
for idx, row in merged_df.iterrows():
        if pd.isna(row['speedup']):
                result.append('-')
        else:
                value = row['estimate'] - row['speedup'] + 1
                result.append(value)

#merged_df['error'] = merged_df.apply(compute, axis=1)
merged_df['error'] = result


result_df = merged_df[['case', 'estimate', 'error']]


result_df.to_csv('estimate.csv', index=False)
