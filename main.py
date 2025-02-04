import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main(results_name : str):
    # get name of scenario
    print(f'Generating plots for: `{results_name}`')

    # creat folder for plots
    plot_dir : str = os.path.join('plots', results_name)
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

    # load csv
    data_path = os.path.join('data', f'{results_name}.csv')
    data : pd.DataFrame = pd.read_csv(data_path)

    # set teams if not in data
    if 'Team' not in data.columns or True:
        team_2 = ['Alan', 'Javi', 'Kazuki', 'Joshua', 'Pryank', 'Roshan']
        teams = []
        for _,row in data.iterrows():
            if row['Player'] in team_2:
                teams.append(2)
            else:
                teams.append(1)
        data['Team'] = teams
        data.to_csv(data_path)
    
    # get list of players and sort alphabetically
    players : list = list(data['Player'].unique())
    players.sort()

    ## RIDGE PLOTS PER HOLE
    plt.figure(figsize=(8,16))
    ax = sns.violinplot(data=data, x='Diff', y='Hole', hue='Course', split=True, orient='h', inner=None, gap=0.1)

    # save plot
    plot_path = os.path.join(plot_dir, f'ridge_holes.png')
    plt.suptitle('Distribution of ΔHits per Hole')
    ax.grid(True)
    plt.savefig(plot_path)
    plt.close()

    ## RIDGE PLOTS PER PLAYER
    plt.figure(figsize=(9,16))
    ax = sns.violinplot(data=data, x='Diff', y='Player', hue='Course', split=True, orient='h', inner=None, gap=0.1)

    # save plot
    plot_path = os.path.join(plot_dir, f'ridge_players.png')
    plt.suptitle('Distribution of ΔHits per Player')
    ax.grid(True)
    plt.savefig(plot_path)
    plt.close()

    ## RIDGE PLOTS PER TEAM
    plt.figure(figsize=(9,16))
    ax = sns.violinplot(data=data, x='Diff', y='Team', hue='Course', split=True, orient='h', inner=None, gap=0.1)

    # save plot
    plot_path = os.path.join(plot_dir, f'ridge_team.png')
    plt.suptitle('Distribution of ΔHits per Team')
    ax.grid(True)
    plt.savefig(plot_path)
    plt.close()

    ## LEADERBOARD TIME-SERIES PER PLAYER
    # calculate data
    ts = [int(v) for v in data['t'].unique()]
    ts.append(0); ts.sort()

    leaderboard = {player : [] for player in players}
    for t_i in ts:
        data_i = [vals for t,*vals in data.values if t <= t_i]
        if len(data_i) == 0 :
            rankings = [player for player in players]
        else:
            # tie-breaker: delta -> total hits -> alphabetical 
            scores_i = [(sum([d for *_,p,_,d,_ in data_i if p==player]), sum([h for *_,p,h,_,_ in data_i if p==player]), player) for player in players]
            scores_i.sort()
            rankings = [player for *_,player in scores_i]

        for player in players:
            leaderboard[player].append(rankings.index(player)+1)
    
    # generate figure
    plt.figure(figsize=(16,9))

    # plot leaderboard time-series
    for player in players: plt.plot(ts, leaderboard[player], marker='o', label=player)

    # plot 18th hole change
    plt.axvline(x=18,label='course change',color='r',ls='--')

    # set format for plot
    plt.grid(True)
    plt.gca().invert_yaxis()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(ts)
    plt.yticks([i+1 for i in range(len(players))])
    plt.ylabel('Ranking')
    plt.xlabel('Hole')
    plt.title('Leaderboard')
    plt.tight_layout()
 
    # save plot
    plot_path = os.path.join(plot_dir, 'leaderboard.png')
    plt.savefig(plot_path)
    plt.close()

    # ## LEADERBOARD TIME-SERIES PER TEAM
    # # calculate data
    # ts = [int(v) for v in data['t'].unique()]
    # ts.append(0); ts.sort()

    # leaderboard = {i+1 : [] for i in range(2)}
    # for t_i in ts:
    #     data_i = [vals for t,*vals in data.values if t <= t_i]
    #     if len(data_i) == 0 :
    #         rankings = [player for player in players]
    #     else:
    #         # tie-breaker: delta -> total hits -> alphabetical 
    #         scores_i = [(sum([d for *_,p,_,d,_ in data_i if p==player]), sum([h for *_,p,h,_,_ in data_i if p==player]), player) for player in players]
    #         scores_i.sort()
    #         rankings = [player for *_,player in scores_i]

    #     for player in players:
    #         leaderboard[player].append(rankings.index(player)+1)
    
    # # generate figure
    # plt.figure(figsize=(16,9))

    # # plot leaderboard time-series
    # for player in players: plt.plot(ts, leaderboard[player], marker='o', label=player)

    # # plot 18th hole change
    # plt.axvline(x=18,label='course change',color='r',ls='--')

    # # set format for plot
    # plt.grid(True)
    # plt.gca().invert_yaxis()
    # plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    # plt.xticks(ts)
    # plt.yticks([i+1 for i in range(len(players))])
    # plt.ylabel('Ranking')
    # plt.xlabel('Hole')
    # plt.title('Leaderboard')
    # plt.tight_layout()
 
    # # save plot
    # plot_path = os.path.join(plot_dir, 'leaderboard_teams.png')
    # plt.savefig(plot_path)
    # plt.close()

    ## ACCUMULATED SCORE DELTA TIME-SERIES
    # calculate data
    ts = [int(v) for v in data['t'].unique()]
    ts.append(0); ts.sort()

    scores = {player : [] for player in players}
    for t_i in ts:
        data_i = [vals for t,*vals in data.values if t <= t_i]
        
        for player in players:
            scores[player].append(sum([d for *_,p,_,d,_ in data_i if p==player]))
    
    # generate figure
    plt.figure(figsize=(16,9))

    # plot scores time-series
    for player in players: plt.plot(ts, scores[player], marker='o', label=player)

    # plot 18th hole change
    plt.axvline(x=18,label='course change',color='r',ls='--')

    # set format for plot
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(ts)
    plt.ylabel('Accumulated ΔHits')
    plt.xlabel('Hole')
    plt.title('Accumulated ΔHits vs time')
    plt.tight_layout()

    # save plot
    plot_path = os.path.join(plot_dir, 'accumulated_scores_delta.png')
    plt.savefig(plot_path)
    plt.close()

    ## ACCUMULATED SCORE TIME-SERIES
    # calculate data
    ts = [int(v) for v in data['t'].unique()]
    ts.append(0); ts.sort()

    scores = {player : [] for player in players}
    for t_i in ts:
        data_i = [vals for t,*vals in data.values if t <= t_i]
        
        for player in players:
            scores[player].append(sum([h for *_,p,h,_,_ in data_i if p==player]))
    
    # generate figure
    plt.figure(figsize=(16,9))

    # plot scores time-series
    for player in players: plt.plot(ts, scores[player], marker='o', label=player)

    # plot 18th hole change
    plt.axvline(x=18,label='course change',color='r',ls='--')

    # set format for plot
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(ts)
    # plt.yticks([i+1 for i in range(max([]))])
    plt.ylabel('Accumulated Hits')
    plt.xlabel('Hole')
    plt.title('Accumulated Hits vs time')
    plt.tight_layout()

    # save plot
    plot_path = os.path.join(plot_dir, 'accumulated_scores.png')
    plt.savefig(plot_path)
    plt.close()

    ## SCORE DELTA TIME-SERIES
    # calculate data
    ts = [int(v) for v in data['t'].unique()]
    ts.append(0); ts.sort()

    scores = {player : [] for player in players}
    for t_i in ts:
        data_i = [vals for t,*vals in data.values if t == t_i]
        
        for player in players:
            scores[player].append(sum([d for *_,p,_,d,_ in data_i if p==player]))

    for player in players:
        # generate figure
        plt.figure(figsize=(16,9))

        # plot scores time-series
        scores_p = [d for t,*_,p,_,d,_ in data.values if p == player]
        scores_p.insert(0,0)
        plt.plot(ts, scores_p, marker='o', label=player)

        # plot 18th hole change
        plt.axvline(x=18,label='course change',color='r',ls='--')

        # set format for plot
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.xticks(ts)
        plt.ylabel('ΔHits')
        plt.xlabel('Hole')
        plt.title('ΔHits vs time')
        plt.tight_layout()

        # save plot
        plot_path = os.path.join(plot_dir, f'scores_delta_{player}.png')
        plt.savefig(plot_path)
        plt.close()
    
    # generate figure
    plt.figure(figsize=(16,9))

    # plot scores time-series
    for player in players: plt.plot(ts, scores[player], marker='o', label=player)

    # plot 18th hole change
    plt.axvline(x=18,label='course change',color='r',ls='--')

    # set format for plot
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(ts)
    plt.ylabel('ΔHits')
    plt.xlabel('Hole')
    plt.title('ΔHits vs time')
    plt.tight_layout()

    # save plot
    plot_path = os.path.join(plot_dir, 'scores_delta.png')
    plt.savefig(plot_path)
    plt.close()

    ## SCORE TIME-SERIES
    # calculate data
    ts = [int(v) for v in data['t'].unique()]
    ts.append(0); ts.sort()

    scores = {player : [] for player in players}
    for t_i in ts:
        data_i = [vals for t,*vals in data.values if t == t_i]
        
        for player in players:
            scores[player].append(sum([h for *_,p,h,_,_ in data_i if p==player]))

    for player in players:
        # generate figure
        plt.figure(figsize=(16,9))

        # plot scores time-series
        scores_p = [h for t,*_,p,h,_,_ in data.values if p == player]
        scores_p.insert(0,0)
        plt.plot(ts, scores_p, marker='o', label=player)

        # plot 18th hole change
        plt.axvline(x=18,label='course change',color='r',ls='--')

        # set format for plot
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.xticks(ts)
        plt.ylabel('Hits')
        plt.xlabel('Hole')
        plt.title('Hits vs time')
        plt.tight_layout()

        # save plot
        plot_path = os.path.join(plot_dir, f'scores_{player}.png')
        plt.savefig(plot_path)
        plt.close()
    
    # generate figure
    plt.figure(figsize=(16,9))

    # plot scores time-series
    for player in players: plt.plot(ts, scores[player], marker='o', label=player)

    # plot 18th hole change
    plt.axvline(x=18,label='course change',color='r',ls='--')

    # set format for plot
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(ts)
    plt.ylabel('Hits')
    plt.xlabel('Hole')
    plt.title('Hits vs time')
    plt.tight_layout()

    # save plot
    plot_path = os.path.join(plot_dir, 'scores.png')
    plt.savefig(plot_path)
    plt.close()
    

if __name__ == "__main__":
    scenario_name : str = "david_fest"
    main(scenario_name)