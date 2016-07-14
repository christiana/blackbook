package blackbook

import groovyx.net.http.HttpResponseException
import groovyx.net.http.RESTClient
import spock.lang.Specification
import spock.lang.Unroll


class PersonValidation extends Specification {
    def static client = new RESTClient('http://localhost:27222')
    def static sharedTripId

    def setupSpec() {
        client.setContentType('application/json')
        def response = client.post path: '/trips',
                body: [
                        name       : "Auto: PersonValidation test",
                        date       : "2016-07-12",
                        description: "Uses for service test"
                ]
        sharedTripId = response.data.id
    }

    def cleanupSpec() {
        client.delete path: "/trips/$sharedTripId"
    }

    @Unroll
    def "POST /trips/#tripId/persons returns 400 BAD REQUEST when weight is not a number"() {
        when:
          client.post path: "/trips/$tripId/persons",
                  body: [
                          weight: 'invalid'
                  ]

        then:
          def ex = thrown(HttpResponseException)
          ex.response.status == 400

        where:
          tripId << [sharedTripId]
    }

}