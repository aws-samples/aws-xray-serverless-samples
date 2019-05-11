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
	"sync"
	"time"
)

//GetCalls generate 'gets' calls for each items
func GetCalls(endpoint string, items, gets int) {
	var wg sync.WaitGroup
	wg.Add(items * gets)

	for i := 0; i < items; i++ {
		uri := fmt.Sprintf("%s/thing%02d", endpoint, i)

		for g := 0; g < gets; g++ {
			go func(uri string) {
				defer wg.Done()
				resp, err := http.Get(uri)
				if err != nil {
					fmt.Printf("PUT %s failed: %s\n", uri, err)
				}

				if resp.StatusCode == 200 {
					fmt.Print(".")
				} else {
					fmt.Print("!")
				}
				resp.Body.Close()
			}(uri)
		}
	}

	wg.Wait()
}

func main() {
	var items, gets int
	flag.IntVar(&items, "items", 10, "Number of items to fetch")
	flag.IntVar(&gets, "count", 50, "Number of get request per item")

	flag.Parse()

	if flag.NArg() < 1 {
		fmt.Printf("Usage: %s [args] endpoint\n", os.Args[0])
		flag.PrintDefaults()
		os.Exit(1)
	}
	fmt.Println(flag.Args())

	endpoint := flag.Arg(0)

	t := time.Now()
	fmt.Printf("GETs for %s\n", endpoint)
	GetCalls(endpoint, items, gets)
	fmt.Printf("\nCompleted %d GETs in: %s\n", items*gets, time.Now().Sub(t))

}
