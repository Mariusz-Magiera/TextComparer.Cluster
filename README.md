# Aplikacja równoległa do projektu z aplikacji internetowych i rozproszonych
To repo zawiera zdockeryzowaną aplikację webową do liczenia procentowego podobieństwa tekstów wprowadzanych na wejściu.
Klaster powstał z wykorzystaniem technologii Apache Spark Standalone Cluster.
Folder ```Docker``` zawiera pliki do uruchamiania aplikacji na dockerze.
Folder ```TextSimilarity``` zawiera kod źródłowy aplikacji.

## Aplikacja
Aplikacja została napisana w języku Scala z wykorzystaniem bibliotek Apache Spark. 
Na wejściu apka oczekuje pliku tekstowego ```input.txt``` który zawiera dokumenty, każdy w jednej linii. 
Apka zwraca procentowe podobieństwo pierwszego dokumentu z każdym dokumentem w pliku.
W celu obliczenia podobieństwa apka liczy wektory TF dla każdego dokumentu na wejściu, normalizuje je i liczy "podobieństwo cosinusów" (cosine similarity) między znormalizowanymi wektorami.
## Docker
### Uruchomienie
Żeby uruchomić aplikację na dockerze należy przejść w terminalu do folderu ```Docker``` i wywołać 2 komendy:
```
$ ./build-images.sh
$ docker-compose up
```
Uruchomienie dockera wymaga Linuxa z zainstalowanymi pakietami ```docker``` i ```docker-compose```.
### Użycie
Aplikacja oferuje proste API RESTowe do liczenia podobieństwa. Do wywołania aplikacji służą endpointy:
* POST: ```http://<host_dockera>:12321```, plik tekstowy w ```request body```
* GET: ```http://<host_dockera>:12321```, uruchomi aplikację na ostatnio wczytanym pliku

Port na którym działa aplikacja można zmienić w pliku ```docker_compose.yml```.