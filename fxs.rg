import "regent"

task inc(data : region(ispace(int3d), double))
where reduces +(data) do
  for x in data do
    data[x] += 1
  end
end

task check_result(data : region(ispace(int3d), double), n_steps : int64, n_tasks : int64)
where reads(data) do
  var expected = double(n_steps * n_tasks)
  for x in data do
    regentlib.assert(data[x] == expected, "mismatch")
  end
  regentlib.c.printf("PASSED\n")
end

task main()
  var data = region(ispace(int3d, { 10, 10, 10 }), double)
  fill(data, 0)

  var n_tasks: int64 = 10
  var n_steps: int64 = 10
  for step = 0, n_steps do
    __demand(__index_launch)
    for color = 0, n_tasks do
      inc(data)
    end
  end
  check_result(data, n_steps, n_tasks)
end
regentlib.start(main)

