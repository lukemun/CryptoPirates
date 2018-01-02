def momentum(crypto_data, alpha):
    vector = 0
    old_vector = 0
    prev = crypto_data.iloc[0]
    actions = [0]
    for i, row in crypto_data[1::].iterrows():
        deriv_perc = (row['weightedAverage'] - prev['weightedAverage'])/(2 * prev['weightedAverage'])
        vector = deriv_perc + alpha * old_vector
        actions.append(vector)
        old_vector = vector
    crypto_data['percMomentum'] = actions
        