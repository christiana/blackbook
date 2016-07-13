package blackbook

import groovyx.net.http.HttpResponseException
import groovyx.net.http.RESTClient
import spock.lang.Specification
import spock.lang.Stepwise

@Stepwise
class TripsCrud extends Specification {

    def client = new RESTClient('http://localhost:27222')
    def id

    def "GET /trips returns status 200"() {
        when:
          def response = client.get path: '/trips'

        then:
          response.status == 200
    }

    def "GET /trips returns application/json content-type"() {
        when:
          def response = client.get path: '/trips'

        then:
          response.contentType == 'application/json'

    }

    def "GET /trips returns an empty list"() {
        when:
          def response = client.get path: '/trips'

        then:
          response.data instanceof List
          response.data.size() == 0

    }

    def "GET /trips/[id] returns 404 NOT FOUND when trip does not exist "() {
        when:
          client.get path: '/trips/1'

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404
    }

    def "GET /trips/[id] returns application/json content-type when trip does not exist "() {
        when:
          client.get path: '/trips/1'

        then:
          def ex = thrown(HttpResponseException)
          ex.response.contentType == 'application/json'
    }

    def "POST /trips returns 201 CREATED and response contains created object id"() {
        when:
          def response = client.post path: '/trips', body: [
                  name: "Første tur",
                  date: "2016-07-12",
                  description: "En fin tur til ålborg"
          ]
          id = response.data.id

        then:
          id
          response.status == 201

    }

    def "GET /trips/[id] returns trips object"() {
        when:
          def response = client.get path: "/trips$id"

        then:
          response.status == 200
          response.data.id == id
          response.data.name == "Første tur"
          response.data.date == "2016-07-12"
          response.data.description == "En fin tur til ålborg"
    }

//    def "PUT /trips/[id] returns 404 NOT FOUND when the trip does not exist"() {
//        when:
//
//    }
//
//    def "PUT /trips/[id] returns 202 ACCEPTED when the trip exists"() {}

}