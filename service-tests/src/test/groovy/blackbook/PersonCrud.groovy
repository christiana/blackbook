package blackbook

import groovyx.net.http.HttpResponseException
import groovyx.net.http.RESTClient
import spock.lang.Specification
import spock.lang.Stepwise
import spock.lang.Unroll

@Stepwise
class PersonCrud extends Specification {

    def static client = new RESTClient('http://localhost:27222')
    def static sharedTripId
    def static sharedPersonId

    def setupSpec() {
        client.setContentType('application/json')
        def response = client.post path: '/trips',
                body: [
                        name       : "Auto: PersonCrud test trip",
                        date       : "2016-07-12",
                        description: "Uses for service test"
                ]
        sharedTripId = response.data.id
    }

    def cleanupSpec() {
        client.delete path: "/trips/$sharedTripId"
    }

    @Unroll
    def "GET /trips/#tripId/persons returns status 200"() {
        when:
          def response = client.get path: "/trips/$tripId/persons"

        then:
          response.status == 200

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    def "GET /trips/#tripId/persons returns an empty list when no persons has been added"() {
        when:
          def response = client.get path: "/trips/$tripId/persons"

        then:
          response.data instanceof List
          response.data.size() == 0

        where:
          tripId << [sharedTripId]

    }

    @Unroll
    def "GET /trips/#tripId/persons/#personId returns 404 NOT FOUND when trip does not exist "() {
        when:
          client.get path: "/trips/$tripId/persons/$personId"

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404

        where:
          tripId << [sharedTripId]
          personId << ['1']

    }


    @Unroll
    def "POST /trips/#tripId/persons returns 201 CREATED and response contains created object id"() {
        when:
          def response = client.post path: "/trips/$tripId/persons",
                  body: [
                          name  : "Reidar Reisgutt",
                          weight: 0.9
                  ]

          sharedPersonId = response.data.id

        then:
          sharedPersonId
          response.status == 201

        where:
          tripId << [sharedTripId]
    }

    @Unroll
    def "GET /trips/#tripId/persons/#personId returns person object"() {
        when:

          def response = client.get path: "/trips/$tripId/persons/$personId"

        then:
          response.status == 200
          response.data.id == personId
          response.data.name == "Reidar Reisgutt"
          response.data.weight == 0.9

        where:
          tripId       | personId
          sharedTripId | sharedPersonId

    }

    @Unroll
    def "GET /trips/#tripId/persons returns a list with one person when one person has been added"() {
        when:
          def response = client.get path: "/trips/$tripId/persons"

        then:
          response.data.size() == 1
          response.data.first() == sharedPersonId

        where:
          tripId       | personId
          sharedTripId | sharedPersonId

    }

    @Unroll
    def "PUT /trips/#tripId/persons/#personId returns 404 NOT FOUND when the person does not exist"() {
        when:
          client.put path: "/trips/$tripId/persons/$personId",
                  body: [
                          name  : "Reidar Reisgutt",
                          weight: 0.9
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 404


        where:
          tripId       | personId
          sharedTripId | 'does_not_exist'

    }
//
//    @Unroll
//    def "PUT /trips/#id returns 202 ACCEPTED when the trip exists"() {
//        when:
//          def response = client.put path: "/trips/$id",
//                  body: [
//                          name       : "Første tur",
//                          date       : "2016-07-12",
//                          description: "En kjip tur til Ålborg"
//                  ]
//
//        then:
//          response.status == 202
//
//        where:
//          id << [sharedTripId]
//
//    }
//
//    @Unroll
//    def "PUT /trips/#id returns 202 ACCEPTED when trip is partially updated"() {
//        when:
//          def response = client.put path: "/trips/$id",
//                  body: [
//                          name: "Tur nr. 1"
//                  ]
//
//        then:
//          response.status == 202
//
//        where:
//          id << [sharedTripId]
//
//    }
//
//    @Unroll
//    def "PUT /trips/#id returns 202 ACCEPTED when an unkown field is sent"() {
//        when:
//          def response = client.put path: "/trips/$id",
//                  body: [
//                          somebadassdata: "I'm so sexy it hurts"
//                  ]
//
//        then:
//          response.status == 202
//
//        where:
//          id << [sharedTripId]
//
//    }
//
//
//    @Unroll
//    def "GET /trips/#id returns updated trip object"() {
//        when:
//          def response = client.get path: "/trips/$id"
//
//        then:
//          response.status == 200
//          response.data.id == id
//          response.data.name == "Tur nr. 1"
//          response.data.date == "2016-07-12"
//          response.data.description == "En kjip tur til Ålborg"
//          response.data.somebadassdata == "I'm so sexy it hurts"
//
//        where:
//          id << [sharedTripId]
//
//    }
//
//    @Unroll
//    def "DELETE /trips/#id returns 404 NOT FOUND when trip does not exist"() {
//        when:
//          client.delete path: "/trips/noexisting"
//
//        then:
//          def ex = thrown(HttpResponseException)
//          ex.response.status == 404
//
//        where:
//          id << [sharedTripId]
//
//    }
//
//    @Unroll
//    def "DELETE /trips/#id returns 202 ACCEPTED when trip exists"() {
//        when:
//          def response = client.delete path: "/trips/$id"
//
//        then:
//          response.status == 202
//
//        where:
//          id << [sharedTripId]
//    }
//
//    @Unroll
//    def "GET /trips/#id returns 404 when trip has been deleted"() {
//        when:
//          client.get path: "/trips/$id"
//
//        then:
//          def ex = thrown(HttpResponseException)
//          ex.response.status == 404
//
//        where:
//          id << [sharedTripId]
//    }

}