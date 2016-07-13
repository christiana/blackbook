package blackbook

import groovyx.net.http.HttpResponseException
import groovyx.net.http.RESTClient
import spock.lang.Specification
import spock.lang.Stepwise
import spock.lang.Unroll

@Stepwise
class TripsCrud extends Specification {

    def client = new RESTClient('http://localhost:27222')
    def static sharedId

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

    def "GET /trips returns an empty list when no trips has been added"() {
        when:
          def response = client.get path: '/trips'

        then:
          response.data instanceof List
          response.data.size() == 0

    }

    @Unroll
    def "GET /trips/#id returns 404 NOT FOUND when trip does not exist "() {
        when:
          client.get path: '/trips/1'

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404

        where:
          id << [sharedId]

    }

    @Unroll
    def "GET /trips/#id returns application/json content-type when trip does not exist "() {
        when:
          client.get path: '/trips/1'

        then:
          def ex = thrown(HttpResponseException)
          ex.response.contentType == 'application/json'

        where:
          id << [sharedId]

    }

    def "POST /trips returns 201 CREATED and response contains created object id"() {
        when:
          def response = client.post path: '/trips', contentType: 'application/json',
                  body: [
                          name       : "Forste tur",
                          date       : "2016-07-12",
                          description: "En fin tur til Aalborg"
                  ]
          sharedId = response.data.id

        then:
          sharedId
          response.status == 201

    }

    @Unroll
    def "GET /trips/#id returns trips object"() {
        when:

          def response = client.get path: "/trips/$id"

        then:
          response.status == 200
          response.data.id == id
          response.data.name == "Forste tur"
          response.data.date == "2016-07-12"
          response.data.description == "En fin tur til Aalborg"

        where:
          id << [sharedId]

    }

    def "GET /trips returns a list with one trip when one trip has been added"() {
        when:
          def response = client.get path: '/trips'

        then:
          response.data.size() == 1
          response.data.first() == sharedId


    }

    def "PUT /trips/[id] returns 404 NOT FOUND when the trip does not exist"() {
        when:
          client.put path: "/trips/doesnotexist", contentType: 'application/json',
                  body: [
                          name       : "Forste tur",
                          date       : "2016-07-12",
                          description: "En fin tur til Aalborg"
                  ]

        then:
          thrown(HttpResponseException)

    }

    @Unroll
    def "PUT /trips/#id returns 202 ACCEPTED when the trip exists"() {
        when:
          def response = client.put path: "/trips/$id", contentType: 'application/json',
                  body: [
                          name       : "Forste tur",
                          date       : "2016-07-12",
                          description: "En kjip tur til Aalborg"
                  ]

        then:
          response.status == 202

        where:
          id << [sharedId]

    }

    @Unroll
    def "PUT /trips/#id returns 202 ACCEPTED when trip is partially updated"() {
        when:
          def response = client.put path: "/trips/$id", contentType: 'application/json',
                  body: [
                          name: "Tur nr. 1"
                  ]

        then:
          response.status == 202

        where:
          id << [sharedId]

    }

    @Unroll
    def "PUT /trips/#id returns 202 ACCEPTED when an unkown field is sent"() {
        when:
          def response = client.put path: "/trips/$id", contentType: 'application/json',
                  body: [
                          somebadassdata: "I'm so sexy it hurts"
                  ]

        then:
          response.status == 202

        where:
          id << [sharedId]

    }


    @Unroll
    def "GET /trips/#id returns updated trip object"() {
        when:
          def response = client.get path: "/trips/$id"

        then:
          response.status == 200
          response.data.id == id
          response.data.name == "Tur nr. 1"
          response.data.date == "2016-07-12"
          response.data.description == "En kjip tur til Aalborg"
          response.data.somebadassdata == "I'm so sexy it hurts"

        where:
          id << [sharedId]

    }

    @Unroll
    def "DELETE /trips/#id returns 404 NOT FOUND when trip does not exist"() {
        when:
          client.delete path: "/trips/noexisting"

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404

        where:
          id << [sharedId]

    }

    @Unroll
    def "DELETE /trips/#id returns 202 ACCEPTED when trip exists"() {
        when:
          def response = client.delete path: "/trips/$id"

        then:
          response.status == 202

        where:
          id << [sharedId]
    }

    @Unroll
    def "GET /trips/#id returns 404 when trip has been deleted"() {
        when:
          client.get path: "/trips/$id"

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404

        where:
          id << [sharedId]
    }

}