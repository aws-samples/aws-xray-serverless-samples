/*
 * Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

//PutCalls create 'items' items at the endpoint
func PutCalls(endpoint string, items int) {
	var wg sync.WaitGroup

	wg.Add(items)

	for i := 0; i < items; i++ {
		uri := fmt.Sprintf("%s/thing%02d", endpoint, i)

		go func(uri string) {
			defer wg.Done()
			req, err := http.NewRequest(http.MethodPut, uri, strings.NewReader("{\"value\": 123, \"something_else\": [1, 2, 3]}"))
			if err != nil {
				fmt.Printf("PUT %s failed: %s\n", uri, err)
			}

			resp, err := http.DefaultClient.Do(req)
			if err != nil {
				fmt.Printf("PUT %s failed: %s\n", uri, err)
			}

			fmt.Printf("PUT %s: %d\n", uri, resp.StatusCode)
			resp.Body.Close()
		}(uri)
	}

	wg.Wait()
}

func main() {
	var items int
	flag.IntVar(&items, "items", 10, "Number of items to fetch")

	flag.Parse()

	if flag.NArg() < 1 {
		fmt.Printf("Usage: %s [args] endpoint\n", os.Args[0])
		flag.PrintDefaults()
		os.Exit(1)
	}
	fmt.Println(flag.Args())

	endpoint := flag.Arg(0)

	t := time.Now()
	fmt.Printf("PUTs for %s\n", endpoint)
	PutCalls(endpoint, items)
	fmt.Printf("Completed %d PUTs in: %s\n\n", items, time.Now().Sub(t))

}
