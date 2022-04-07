import src.ekstraclass.ekstraclass_06_team_optimatisation_transfers as transfers

round = 28
season = '2021_2022'

transfers.main(team_name='algolrytm_01', season=season, round = round, points_type = 'all', sub_factor=0.1,
               budget_now=0.1)
# transfers.main(team_name='algolrytm_02', season=season, round = round, points_type = 'all', sub_factor=0.9,
#               budget_now=0.0)
# transfers.main(team_name='algolrytm_03', season=season, round = round, points_type = '05', sub_factor=0.5,
#                budget_now=0.3)
# transfers.main(team_name='algolrytm_04', season=season, round = round, points_type = '10', sub_factor=0.5,
#                budget_now=0.0)
# transfers.main(team_name='algolrytm_05', season=season, round = round, points_type = '15', sub_factor=0.5,
#                budget_now=0.0)

