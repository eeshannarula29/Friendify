"""File contains Recommendation graph class"""
from __future__ import annotations

from typing import Any
from random import choice

import logging
import webbrowser

import dash
import dash_html_components as html
import dash_cytoscape as cyto
import dash_core_components as dcc
from dash.dependencies import Input, Output

from authenticate import DataHandler
import constants


class _Vertex:
    """A vertex in a friend recommendation graph, is used to represent a user or a preference.

    Each vertex item is either a user id or preference. Both are represented as strings


    Instance Attributes:
        - item: The data stored in this vertex, representing a user or preference.
        - kind: The type of this vertex: 'user' or 'preference'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'preference'}
        """

    item: Any
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'preference'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def similarity_score(self, other: _Vertex) -> float:
        """Return the similarity score between this vertex and other.
        """
        if self.degree() != 0 and other.degree() != 0:
            common_neighbours = {neighbour for neighbour in
                                 self.neighbours.intersection(other.neighbours)
                                 if neighbour.kind == 'preference'}

            all_neighbours = {neighbour for neighbour in
                              self.neighbours.union(other.neighbours)
                              if neighbour.kind == 'preference'}

            numerator = len(common_neighbours)
            denominator = len(all_neighbours)

            return numerator / denominator
        else:
            return 0

    def generate_graph(self, d: int, visited: set[_Vertex]) -> set[_Vertex]:
        """ Return set of all vertices until depth d

        :param visited: the set of already visited vertices
        :param d: the depth
        """
        if d == 0:
            visited.add(self)
            return visited
        else:
            visited.add(self)

            for neighbour in self.neighbours:
                if neighbour.kind == 'user' and neighbour not in visited:
                    visited = visited.union(neighbour.generate_graph(d - 1, visited))

            return visited

    def format_for_graph(self, visited: set[_Vertex]) -> list[dict]:
        """ Return formatted data for visualization

        :param visited: a set of already visited vertices
        """

        networks = [{'data': {'id': self.item, 'label': self.item}}]

        visited.add(self)

        for neighbour in self.neighbours:
            if neighbour not in visited:
                networks.extend(neighbour.format_for_graph(visited))
                networks.append({'data': {'source': self.item, 'target': neighbour.item}})

        return networks


class Graph:
    """A graph used to represent a friend recommendation network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'preference'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'preference'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def get_similarity_score(self, item1: Any, item2: Any) -> float:
        """Return the similarity score between the two given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            return v1.similarity_score(v2)
        else:
            raise ValueError

    def recommend_friends(self, user: str, limit: int) -> list[str]:
        """Return a list of up to <limit> recommended friends based on similarity to the given user.

        The return value is a list of users, sorted in *descending order* of similarity score.

        The returned list should NOT contain:
            - the input user itself
            - any user with a similarity score of 0 to the input user
            - any duplicates
            - any vertices that represents a preference (instead of a user)

        Up to <limit> users are returned, starting with the user with the highest similarity score,
        then the second-highest similarity score, etc. Fewer than <limit> users are returned if
        and only if there aren't enough users that meet the above criteria.

        Preconditions:
            - user in self._vertices
            - self._vertices[user].kind == 'user'
            - limit >= 1
        """
        users = []

        user_vertex = self._vertices[user]

        for vertex in self._vertices:

            other_vertex = self._vertices[vertex]

            if other_vertex.kind == 'user' and \
                    vertex != user and \
                    other_vertex not in user_vertex.neighbours:

                score = user_vertex.similarity_score(other_vertex)

                if score != 0:
                    users.append((score, vertex))

        users.sort(reverse=True)

        return [user_data[1] + f' ({round(user_data[0] * 100)}% match)'
                for user_data in users][:limit]

    def generate_users_graph_for_user(self, user: str, d: int) -> Graph:
        """ Return a graph of a users and their friends until depth d

        :param user: the user ID of the user
        :param d: the depth
        """
        if user not in self._vertices:
            raise ValueError

        vertices = self._vertices[user].generate_graph(d, set())

        graph = Graph()

        for vertex in vertices:
            graph.add_vertex(vertex.item, vertex.kind)

        for vertex in vertices:
            for neighbour in vertex.neighbours:
                if neighbour.item in graph._vertices:
                    graph.add_edge(vertex.item, neighbour.item)

        return graph

    def format_for_graph(self) -> list[dict]:
        """ Return formatted data for visualization
        """
        vertex = self._vertices[choice(list(self._vertices.keys()))]
        return vertex.format_for_graph(set())

    def plot(self) -> None:
        """ Plot the graph in dash
        """
        graph_data = self.format_for_graph()

        app = dash.Dash(__name__)

        log = logging.getLogger('werkzeug')
        log.disabled = True

        @app.callback(Output('cytoscape', 'layout'),
                      Input('dropdown', 'value'))
        def update_layout(layout: Any) -> dict:
            return {
                'name': layout,
                'animate': True
            }

        app.layout = html.Div([
            html.P("Friendify Network"),
            dcc.Dropdown(
                id='dropdown',
                value='cose',
                clearable=False,
                options=[
                    {'label': name.capitalize(), 'value': name}
                    for name in ['breadthfirst', 'grid', 'random', 'circle', 'cose',
                                 'concentric']
                ]
            ),
            cyto.Cytoscape(
                id='cytoscape',
                elements=graph_data,
                layout={'name': 'breadthfirst'},
                style={'width': '1500px', 'height': '800px'}
            ),
        ])

        webbrowser.open_new('http://127.0.0.1:5050/')
        app.run_server(port=5050)

    @staticmethod
    def load_friends_graph(handler: DataHandler) -> Graph:
        """Return a friend recommendation graph from firebase could data using a handler

        The friend recommendation graph stores one vertex for each user and preference in the
        firebase data. Each vertex stores as its item either a user ID or a preference. Edges
        represent a liking of a preference by a user.
        """
        graph = Graph()

        for category in constants.CATEGORIES:
            for preference in constants.CATEGORIES[category]:
                graph.add_vertex(preference, 'preference')

        users = handler.get_all_data()

        for user in users:
            graph.add_vertex(user['userID'], 'user')

            for movie in user['movies']:
                graph.add_edge(user['userID'], movie)

            for music in user['music']:
                graph.add_edge(user['userID'], music)

            for food in user['food']:
                graph.add_edge(user['userID'], food)

            for game in user['games']:
                graph.add_edge(user['userID'], game)

        for user in users:

            for friend in user['friends']:
                graph.add_edge(user['userID'], friend)

        return graph


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['authenticate',
                          'constants',
                          'typing',
                          'random',
                          'logging',
                          'webbrowser',
                          'dash',
                          'dash_html_components',
                          'dash_cytoscape',
                          'dash_core_components',
                          'dash.dependencies'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
