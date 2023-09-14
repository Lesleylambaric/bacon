"""
6.1010 Spring '23 Lab 3: Bacon Number
"""

#!/usr/bin/env python3

import pickle

kevin = 4724


def transform_data(raw_data):
    """Takes in the raw data and transforms it into a list of
    two dictionaries,the first dictionary takes in an actor_id as the key
    and inputs the actors they acted with as the value
    The second dictionary takes in a film ID as the key
    and inputs the actors that acted in the film as
    the values"""
    actors = {}
    film_act = {}
    for a1, a2, film in raw_data:
        if a1 not in actors:
            actors[a1] = {a2}
        else:
            actors[a1].add(a2)

        if a2 not in actors:
            actors[a2] = {a1}
        else:
            actors[a2].add(a1)

        if film not in film_act:
            film_act[film] = {a2, a1}
        else:
            film_act[film].add(a2)
            film_act[film].add(a1)
            #film_act[film].add(a1)

    return [actors, film_act]


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """Checks if the actors acted together, and return True if they
    acted together and False if they did not"""
    if actor_id_1 == actor_id_2:
        return True
    else:
        actors = transformed_data[0]
        return actor_id_2 in actors.get(actor_id_1, set())


def actors_with_bacon_number(transformed_data, n):
    """Takes in a bacon number and returns
    the set of actors with that bacon number"""
    seen = {4724}
    actors_n=[(4724,0)]
    bacon_path=set()
    actors=transformed_data[0]

    if n == 0:
        return 4724
    while actors_n:
        actor_id,bacon=actors_n.pop(0)
        if bacon==n:
            bacon_path.add(actor_id)
        elif bacon<n:
            for co_actor in actors[actor_id]:
                if co_actor not in seen:
                    seen.add(co_actor)
                    actors_n.append((co_actor,bacon+1))
    return bacon_path


def bacon_path(transformed_data, actor_id):
    """Takes in an actor_id and returns the path
    from Kevin Bacon to them"""
    
    return actor_to_actor_path(transformed_data, 4724, actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """Takes in two actor_ids and returns the path
    from one actor_id_1 to actor_id_2"""

    actors = transformed_data[0]
    start = actor_id_1
    dest = actor_id_2

    queue = [(start, [start])]
    visited = set([start])
    count=0 #keep track of iterations so the function doesn't get stuck in an infinite loop

    while queue:
        actor, path = queue.pop(0)
        if actor == dest:
            return path
        if count> len(actors):
            return None
        else:
            for co_actor in actors[actor]:
                if co_actor not in visited:
                    visited.add(co_actor)
                    queue.append((co_actor, path + [co_actor]))
                if co_actor == dest:
                    return path + [co_actor]
        count += 1
    return None
# f=open("resources/large.pickle", "rb")
# smalldb=pickle.load(f)
# smalldb=transform_data(smalldb)

# print(actor_to_actor_path(smalldb,1245,1338716 ))
def get_movie_path(transformed_data,actor_name_1,actor_name_2):
    with open("resources/movies.pickle",'rb') as db:
        movies=pickle.load(db)
    with open('resources/names.pickle','rb') as db:
        names=pickle.load(db)

    actor_id_1 = names[actor_name_1]
    actor_id_2=names[actor_name_2]
    path=actor_to_actor_path(transformed_data,actor_id_1,actor_id_2)

    films_cast= transformed_data[1]
    films=films_cast.keys()

    movie_path=[j for i in range(len(path)-1)
                        for j in films
                            if path[i] in films_cast[j] and path[i+1] in films_cast[j]]
    result=[j for i in movie_path
                for j in movies
                    if movies[j]==i]
    return result


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """"""
    actors = transformed_data[0]
    paths=[]
    if goal_test_function(actor_id_1):
        return [actor_id_1]
    
    
    for goal in actors.keys():
        if goal_test_function(goal):
            paths.append(actor_to_actor_path(transformed_data,actor_id_1,goal))
    if len(paths) > 0:   
        return min(paths,key=len)
    else:
        return None

def actors_connecting_films(transformed_data, film1, film2):
    """Gives the shortest path(from an actor in film 1 to film2)
    from film1 to film2"""
    films = transformed_data[1]
    start = films[film1]  # a set of actors in film 1
    dest = films[film2]  # a set of actors in film2

    paths = []
    for actor1 in start:
        for actor2 in dest:
            paths.append(actor_to_actor_path(transformed_data, actor1, actor2))
    if len(paths) > 0:
        return min(paths, key=len)
    return None


# f=open("resources/large.pickle", "rb")
# smalldb=pickle.load(f)
# smalldb=transform_data(smalldb)

# print(actors_connecting_films(smalldb,1245,1338716 ))


if __name__ == "__main__":
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
    # f=open("resources/movies.pickle", "rb")
    # smalldb=pickle.load(f)
    # print(transform_data(smalldb)[1])
    # print(smalldb)
    # #print(smalldb['Andy Grace'])
    # for k,v in smalldb.items():
    #     if k=='Apollo 13' :
    #         print(v)
    # def case1():
    #     f = open("resources/names.pickle", "rb")
    #     names = pickle.load(f)
    #     ds = [1389010, 1267814, 562179, 21315, 9207, 953997]
    #     name = []
    #     for d in ds:
    #         for k, v in names.items():
    #             if v == d:
    #                 name.append(k)
    #     return name

    # print(case1())
    # def case2():
    #     f=open("resources/large.pickle", "rb")
    #     db_small=pickle.load(f)
    #     print(actor_to_actor_path(transform_data(db_small),1389010,953997))
    # print(case2())

    # v=pickle.load(f)
    # print(v)
    # f=open("resources/large.pickle", "rb")
    # db_small=pickle.load(f)
    # print(bacon_path(transform_data(db_small),1442725))
    # #print(db_small)

    # f=open('resources/names.pickle','rb')
    # names=pickle.load(f)
    # for k,v in names.items():
    #     if k=='Sven Batinic':
    #         print (v)
    
    # f=open("resources/large.pickle", "rb")
    # smalldb=pickle.load(f)
    # smalldb=transform_data(smalldb)
    # films=smalldb[1]
    
    # for k,v in films.items():
    #     if 1338716 and 1338712 in v:
    #         print(k)

