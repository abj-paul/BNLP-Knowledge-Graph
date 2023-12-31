document.addEventListener("DOMContentLoaded", function () {
    const cy = cytoscape({
      container: document.getElementById('cy'),
      elements: [
        { data: { id: 'Paper1', type: 'paper' } },
        { data: { id: 'Paper2', type: 'paper' } },
        { data: { id: 'Dataset1', type: 'dataset' } },
        { data: { id: 'Topic1', type: 'topic' } },
        { data: { id: 'Paper1_to_Paper2', source: 'Paper1', target: 'Paper2' } },
        { data: { id: 'Paper1_to_Dataset1', source: 'Paper1', target: 'Dataset1' } },
        { data: { id: 'Paper1_to_Topic1', source: 'Paper1', target: 'Topic1' } },
      ],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#ccc',
            'label': 'data(id)'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#555'
          }
        }
      ],
      layout: {
        name: 'grid',
        rows: 1
      }
    });
  });
  