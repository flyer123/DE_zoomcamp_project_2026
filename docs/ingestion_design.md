<h3>Ingestion Design</h3>

<h4>File name structure and format</h4>
<ul>
  <li><p>flight_list_yearmonth.parquet</p></li>
  <li><p>Those files will stay in parquet format</p></li>
  <li><p>Files will be transformed, columns `year`, `month`, `day` will be derived from `first_seen` column</p></li>
</ul>
<h4>Folder structure</h4>

    data-lake/
      bronze/
        flights/
          year=2024/
            month=03/
              day=01/
                part-000.parquet
